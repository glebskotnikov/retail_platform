import logging
import os.path

from django.contrib.auth import get_user_model, password_validation
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueValidator

from config import settings
from electronics.models import Role
from electronics.validators import validate_supplier_role

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    role = serializers.PrimaryKeyRelatedField(queryset=Role.objects.all())
    role_type = serializers.CharField(source="role.role_type")
    supplier = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "name",
            "country",
            "city",
            "street",
            "house_number",
            "role",
            "role_type",
            "supplier",
        )
        read_only_fields = ("debt",)

    def get_supplier(self, obj):
        role_instance = obj.role
        if role_instance.supplier:
            supplier_data = {
                "supplier_id": role_instance.supplier.user.id,
                "supplier_name": role_instance.supplier.user.name,
            }
            return supplier_data

        return None

    def validate(self, attrs):
        supplier = attrs.get("supplier")
        user_role_type = attrs.get("role_type")

        if supplier:
            supplier_role_type = Role.objects.get(user_id=supplier.id).role_type

            validate_supplier_role(supplier_role_type, user_role_type)

        return attrs


class UserRegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(min_length=8, write_only=True)
    role_type = serializers.ChoiceField(choices=Role.ROLE_TYPE_CHOICES)
    supplier = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), write_only=True, required=False
    )

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "password",
            "name",
            "country",
            "city",
            "street",
            "house_number",
            "role_type",
            "supplier",
        )

    def create(self, validated_data):
        password = validated_data.pop("password")
        role_type = validated_data.pop("role_type")
        supplier_id = validated_data.pop("supplier", None)

        if supplier_id:
            supplier_role_type = Role.objects.get(user_id=supplier_id.id).role_type

            validate_supplier_role(supplier_role_type, role_type)

        if role_type == "Admin":
            raise serializers.ValidationError("Users cannot register as admin")

        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()

        role = Role.objects.create(user=user, role_type=role_type)

        if supplier_id is not None:
            supplier_role = Role.objects.get(user_id=supplier_id.id)
            role.supplier = supplier_role
            role.save()

        return UserSerializer(user).data


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        try:
            User.objects.get(email=value)
        except User.DoesNotExist:
            raise ValidationError("User with given email does not exist")
        return value

    def save(self):
        email = self.validated_data["email"]
        user = User.objects.get(email=email)

        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))

        # create reset password url
        domain = "http://localhost:8000"
        reset_password_url = f"{domain}/change-password/{uid}/{token}"

        # load email template
        message = render_to_string(
            os.path.join(
                settings.BASE_DIR, "templates/users/password_reset_email.html"
            ),
            {"user": user, "reset_password_url": reset_password_url},
        )

        send_mail("Password Reset", message, None, [email])


class PasswordResetConfirmSerializer(serializers.Serializer):
    uid = serializers.CharField()
    token = serializers.CharField()
    new_password = serializers.CharField()

    def validate(self, data):
        try:
            uid = force_str(urlsafe_base64_decode(data["uid"]))
            user = User.objects.get(pk=uid)
        except (User.DoesNotExist, ValueError, TypeError, OverflowError):
            raise serializers.ValidationError(
                {
                    "uid": ["Invalid value"],
                }
            )

        if not default_token_generator.check_token(user, data["token"]):
            raise serializers.ValidationError(
                {
                    "token": ["Invalid value"],
                }
            )

        password_validation.validate_password(data["new_password"], user)

        return data

    def save(self):
        new_password = self.validated_data["new_password"]
        uid = force_str(urlsafe_base64_decode(self.validated_data["uid"]))
        user = User.objects.get(pk=uid)
        user.set_password(new_password)
        user.save()
        return user
