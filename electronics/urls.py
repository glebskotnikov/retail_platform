from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .apps import ElectronicsConfig
from .views import RoleViewSet

app_name = ElectronicsConfig.name

router = DefaultRouter()
router.register(r"roles", RoleViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
