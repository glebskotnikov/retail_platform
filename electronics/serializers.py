from rest_framework import serializers

from .models import Role
from .validators import validate_supplier_role


class RoleSerializer(serializers.ModelSerializer):
    products = serializers.StringRelatedField(many=True)

    class Meta:
        model = Role
        fields = "__all__"

    def update(self, instance, validated_data):
        validated_data.pop("debt", None)
        return super().update(instance, validated_data)

    def validate(self, attrs):
        supplier = attrs.get("supplier")
        user_role_type = attrs.get("role_type")

        if supplier:
            supplier_role_type = Role.objects.get(user_id=supplier.id).role_type

            validate_supplier_role(supplier_role_type, user_role_type)

        return attrs

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["role_name"] = instance.role_type
        return representation
