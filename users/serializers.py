from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from electronics.models import Role
from electronics.validators import validate_admin_role, validate_supplier_role

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


class UserRegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(min_length=8, write_only=True)
    role_type = serializers.ChoiceField(
        choices=Role.ROLE_TYPE_CHOICES, validators=[validate_admin_role]
    )
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
        supplier = validated_data.pop("supplier", None)

        user = User.objects.create(**validated_data)

        if role_type.lower() == "employee":
            user.is_staff = True
            user.is_active = True

        user.set_password(password)
        user.save()

        role = Role.objects.create(user=user, role_type=role_type)

        if supplier is not None:
            supplier_role = Role.objects.get(user_id=supplier.id)
            role.supplier = supplier_role
            role.save()

        return UserSerializer(user).data

    def validate(self, attrs):
        role_type = attrs.get("role_type")
        supplier = attrs.get("supplier")

        if supplier:
            supplier_role_type = supplier.role.role_type

            validate_supplier_role(supplier_role_type, role_type)

        return attrs
