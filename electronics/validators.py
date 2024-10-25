from rest_framework import serializers


def validate_supplier_role(supplier_role_type, user_role_type):
    if user_role_type == "Factory" and supplier_role_type != None:
        raise serializers.ValidationError("Factory cannot have any supplier")
    elif user_role_type == "RetailChain" and supplier_role_type not in [
        "Factory",
        "RetailChain",
    ]:
        raise serializers.ValidationError(
            "RetailChain can only have Factory or RetailChain as a supplier"
        )
