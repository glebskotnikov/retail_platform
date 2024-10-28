from rest_framework import serializers


def validate_supplier_role(supplier_role_type, user_role_type):
    allowed_supplier_map = {
        "factory": [],
        "employee": [],
        "retailchain": ["factory", "retailchain"],
        "individualentrepreneur": ["factory", "retailchain", "individualentrepreneur"],
    }

    allowed_suppliers = allowed_supplier_map.get(user_role_type.lower())

    if supplier_role_type.lower() not in allowed_suppliers:
        raise serializers.ValidationError(
            f"{user_role_type} can only have {allowed_suppliers} as a supplier"
        )


def validate_admin_role(role_type):
    if role_type.lower() == "admin":
        raise serializers.ValidationError("Users cannot register as admin")
    return role_type
