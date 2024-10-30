from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import filters, viewsets

from users.permissions import IsActiveEmployee

from .models import Role
from .serializers import RoleSerializer


@extend_schema(tags=["Roles"])
@extend_schema_view(
    list=extend_schema(
        summary="Getting a list of all roles",
    ),
    create=extend_schema(
        summary="Creating a new role",
    ),
    update=extend_schema(
        summary="Modifying an existing role",
    ),
    partial_update=extend_schema(
        summary="Making partial changes to a role",
    ),
    retrieve=extend_schema(
        summary="Retrieving detailed information about a role",
    ),
    destroy=extend_schema(
        summary="Deleting a role",
    ),
)
class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    filterset_fields = ["user__country"]
    search_fields = ["user__country", "user__city", "user__street"]
    permission_classes = [IsActiveEmployee]
