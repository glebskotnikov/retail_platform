from drf_spectacular.utils import extend_schema
from rest_framework import permissions, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from .serializers import (PasswordResetConfirmSerializer,
                          PasswordResetSerializer, UserRegisterSerializer, UserSerializer)


@extend_schema(
    tags=["Users"],
    summary="Register a new user",
)
class RegisterUserView(APIView):
    """
    API endpoint that allows new users to register.
    """

    permission_classes = [permissions.AllowAny]
    serializer_class = UserRegisterSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user_data = serializer.save()
            return Response(
                {
                    "user": user_data,
                    "message": "User created successfully",
                },
                status=status.HTTP_201_CREATED,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    tags=["Users"],
    summary="Password reset",
)
class PasswordResetView(APIView):
    """
    API view for initiating a password reset request.
    """

    permission_classes = [permissions.AllowAny]
    serializer_class = PasswordResetSerializer

    def post(self, request):
        serializer = PasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"detail": "Password reset e-mail sent"},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    tags=["Users"],
    summary="Confirming a password reset",
)
class PasswordResetConfirmView(APIView):
    """
    API view for confirming a password reset request.
    """

    permission_classes = [permissions.AllowAny]
    serializer_class = PasswordResetConfirmSerializer

    def post(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"detail": "Password has been reset with the new password."},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    tags=["Users"],
    summary="Login a user and obtain token pair",
)
class CustomTokenObtainPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)


@extend_schema(
    tags=["Users"],
    summary="Refresh token",
)
class CustomTokenRefreshView(TokenRefreshView):
    permission_classes = (AllowAny,)
