import pytest
from rest_framework.test import APIClient

from electronics.models import Role
from users.models import User


# A fixture providing an API client
@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def role_data_admin():
    return {
        "role_type": "admin",
    }


@pytest.fixture
def role_data_employee():
    return {
        "role_type": "employee",
    }


@pytest.fixture
def role_data_factory():
    return {
        "role_type": "factory",
    }


@pytest.fixture
def role_data_retail_chain():
    return {
        "role_type": "retailchain",
    }


@pytest.fixture
def role_data_ind_ent():
    return {
        "role_type": "individualentrepreneur",
    }


@pytest.fixture
def test_factory_user(db, role_data_factory):
    factory_user = User.objects.create(
        email="test_factory_user@test.com",
        name="test_factory_user",
    )
    factory_user.set_password("testpassword")
    factory_user.save()
    Role.objects.create(user=factory_user, **role_data_factory)
    return factory_user


@pytest.fixture
def test_retail_chain_user(db, role_data_retail_chain):
    retail_chain_user = User.objects.create(
        email="test_retail_chain_user@test.com",
        name="test_retail_chain_user",
    )
    retail_chain_user.set_password("testpassword")
    retail_chain_user.save()
    Role.objects.create(user=retail_chain_user, **role_data_retail_chain)
    return retail_chain_user


@pytest.fixture
def test_ind_ent_user(db, role_data_ind_ent):
    ind_ent_user = User.objects.create(
        email="test_ind_ent_user@test.com",
        name="test_ind_ent_user",
    )
    ind_ent_user.set_password("testpassword")
    ind_ent_user.save()
    Role.objects.create(user=ind_ent_user, **role_data_ind_ent)
    return ind_ent_user


@pytest.fixture
def test_employee_user(db, role_data_employee):
    employee_user = User.objects.create(
        email="test_employee_user@test.com",
        name="test_employee_user",
        is_staff=True,
        is_active=True,
    )
    employee_user.set_password("testpassword")
    employee_user.save()
    Role.objects.create(user=employee_user, **role_data_employee)
    return employee_user


@pytest.fixture
def test_user_data(db):
    return {
        "email": "test_user_data@email.com",
        "password": "testpassword",
        "name": "test_user_data",
    }
