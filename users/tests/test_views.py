from rest_framework_simplejwt.tokens import RefreshToken

from users.models import User


def test_user_create_view(api_client, test_user_data, role_data_factory):
    data = {**test_user_data, "role_type": role_data_factory["role_type"]}
    response = api_client.post("/users/users/", data, format='json')
    assert response.status_code == 201
    assert 'user' in response.data
    assert 'message' in response.data
    assert response.data['message'] == "User created successfully"


def test_perform_update(api_client, test_employee_user, test_retail_chain_user):
    api_client.force_authenticate(user=test_employee_user)
    data = {
        'name': 'new_test_name'
    }
    response = api_client.patch(f"/users/users/{test_retail_chain_user.id}/", data, format='json')
    assert response.status_code == 200
    assert response.data['name'] == 'new_test_name'


def test_create_user_with_invalid_data(api_client):
    data = {
        'username': '',
        'password': 'short',
        'role_type': 'unknown_role_type'
    }
    response = api_client.post("/users/users/", data, format='json')
    assert response.status_code == 400


def test_custom_token_obtain_pair_view(api_client, test_user_data):
    user = User(email=test_user_data['email'])
    user.set_password(test_user_data['password'])
    user.save()

    data = {
        'email': test_user_data['email'],
        'password': test_user_data['password']
    }
    response = api_client.post("/users/login/", data, format='json')
    assert response.status_code == 200
    assert 'access' in response.data
    assert 'refresh' in response.data


def test_custom_token_refresh_view(api_client, test_user_data):
    user = User(email=test_user_data['email'])
    user.set_password(test_user_data['password'])
    user.save()

    refresh = RefreshToken.for_user(user)
    data = {'refresh': str(refresh)}
    response = api_client.post("/users/token/refresh/", data, format='json')
    assert response.status_code == 200
    assert 'access' in response.data
