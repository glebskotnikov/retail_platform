from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import status, viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from .models import User
from .permissions import IsActiveEmployee
from .serializers import UserRegisterSerializer, UserSerializer


@extend_schema(tags=["Users"])
@extend_schema_view(
    list=extend_schema(
        summary="Getting a list of all users",
    ),
    create=extend_schema(
        summary="Registering a new user",
    ),
    update=extend_schema(
        summary="Modifying an existing user",
    ),
    partial_update=extend_schema(
        summary="Making partial changes to a user",
    ),
    retrieve=extend_schema(
        summary="Retrieving detailed information about a user",
    ),
    destroy=extend_schema(
        summary="Deleting a user",
    ),
)
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsActiveEmployee]

    def perform_update(self, serializer):
        data = serializer.validated_data
        data.pop("debt", None)
        serializer.save(**data)

    def create(self, request):
        serializer = UserRegisterSerializer(data=request.data)
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

    def get_permissions(self):
        if self.action == "create":
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsActiveEmployee]
        return [permission() for permission in permission_classes]


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
