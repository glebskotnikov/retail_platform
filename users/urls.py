from django.urls import path

from users.apps import UsersConfig
from users.views import (CustomTokenObtainPairView, CustomTokenRefreshView,
                         PasswordResetConfirmView, PasswordResetView,
                         RegisterUserView)

app_name = UsersConfig.name

urlpatterns = [
    # users
    path("register/", RegisterUserView.as_view(), name="register"),
    path("reset_password/", PasswordResetView.as_view(), name="reset_password"),
    path(
        "reset_password_confirm/",
        PasswordResetConfirmView.as_view(),
        name="reset_password_confirm",
    ),
    # token
    path(
        "login/",
        CustomTokenObtainPairView.as_view(),
        name="login",
    ),
    path(
        "token/refresh/",
        CustomTokenRefreshView.as_view(),
        name="token_refresh",
    ),
]
