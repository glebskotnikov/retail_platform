import pytest
from rest_framework.exceptions import ValidationError

from users.models import User
from users.serializers import UserRegisterSerializer, UserSerializer


@pytest.mark.django_db
def test_user_serializer_without_supplier(test_factory_user):
    user_serializer = UserSerializer(test_factory_user)
    assert user_serializer.data["supplier"] is None


@pytest.mark.django_db
def test_user_serializer_with_supplier(
        test_factory_user, test_retail_chain_user, role_data_retail_chain
):
    test_retail_chain_user.role.supplier = test_factory_user.role
    test_retail_chain_user.role.role_type = role_data_retail_chain["role_type"]
    test_retail_chain_user.role.save()

    user_serializer = UserSerializer(test_retail_chain_user)

    assert "supplier" in user_serializer.data
    assert user_serializer.data["supplier"] == {
        "supplier_id": test_factory_user.id,
        "supplier_name": test_factory_user.name,
    }


@pytest.mark.django_db
def test_user_register_serializer_with_valid_data(test_user_data, role_data_factory):
    data = {**test_user_data, "role_type": role_data_factory["role_type"]}
    user_register_serializer = UserRegisterSerializer(data=data)

    assert user_register_serializer.is_valid()


@pytest.mark.django_db
def test_user_register_serializer_with_invalid_data(test_user_data):
    user_register_serializer = UserRegisterSerializer(data=test_user_data)

    assert not user_register_serializer.is_valid()


@pytest.mark.django_db
def test_user_register_serializer_with_admin_role(test_user_data, role_data_admin):
    test_user_data["role_type"] = "admin"
    user_register_serializer = UserRegisterSerializer(data=test_user_data)

    assert not user_register_serializer.is_valid()
    assert "role_type" in user_register_serializer.errors
    assert (
            "Users cannot register as admin" in user_register_serializer.errors["role_type"]
    )


@pytest.mark.django_db
def test_user_register_serializer_with_incompatible_supplier(
        test_user_data, test_retail_chain_user, role_data_factory
):
    data = {
        **test_user_data,
        "role_type": role_data_factory["role_type"],
        "supplier": test_retail_chain_user.id,
    }
    user_register_serializer = UserRegisterSerializer(data=data)
    with pytest.raises(ValidationError):
        user_register_serializer.is_valid(raise_exception=True)


@pytest.mark.django_db
def test_create_with_non_employee_role(test_user_data, role_data_factory):
    data = {**test_user_data, "role_type": role_data_factory["role_type"]}
    user_register_serializer = UserRegisterSerializer(data=data)
    if not user_register_serializer.is_valid():
        print(user_register_serializer.errors)
    assert user_register_serializer.is_valid()
    created_user_data = user_register_serializer.save()
    created_user = User.objects.get(id=created_user_data["id"])
    assert created_user.is_staff is False
    assert created_user.is_active is True


@pytest.mark.django_db
def test_create_with_no_supplier(test_user_data, role_data_employee):
    data = {**test_user_data, "role_type": role_data_employee["role_type"]}
    user_register_serializer = UserRegisterSerializer(data=data)
    assert user_register_serializer.is_valid()
    created_user_data = user_register_serializer.save()
    assert created_user_data["supplier"] is None


@pytest.mark.django_db
def test_user_register_serializer_with_valid_data_and_supplier(
        test_user_data, role_data_retail_chain, test_factory_user
):
    data = {
        **test_user_data,
        "role_type": role_data_retail_chain["role_type"],
        "supplier": test_factory_user.id,
    }
    user_register_serializer = UserRegisterSerializer(data=data)
    assert user_register_serializer.is_valid()
    created_user_data = user_register_serializer.save()
    assert created_user_data["supplier"]
    assert created_user_data["supplier"] == {
        "supplier_id": test_factory_user.id,
        "supplier_name": test_factory_user.name,
    }
