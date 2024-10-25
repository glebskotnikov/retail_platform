from django.db import models
from rest_framework.exceptions import ValidationError

from users.models import User

NULLABLE = {"blank": True, "null": True}


class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name="product name")
    model = models.CharField(max_length=255, verbose_name="model")
    release_date = models.DateField(verbose_name="release date")

    class Meta:
        verbose_name = "product"
        verbose_name_plural = "products"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Role(models.Model):
    ROLE_TYPE_CHOICES = [
        ("Admin", "Admin"),
        ("Factory", "Factory"),
        ("RetailChain", "Retail Chain"),
        ("IndividualEntrepreneur", "Individual Entrepreneur"),
    ]

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="role", verbose_name="user"
    )
    products = models.ManyToManyField(Product, blank=True, verbose_name="products")
    supplier = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        related_name="suppliers",
        **NULLABLE,
        verbose_name="supplier",
    )
    role_type = models.CharField(
        max_length=30, choices=ROLE_TYPE_CHOICES, verbose_name="role type"
    )

    class Meta:
        verbose_name = "Role"
        verbose_name_plural = "Roles"
        ordering = ["user"]

    def __str__(self):
        return f"{self.user.name} ({self.role_type})"

    def get_hierarchy_level(self):
        HIERARCHY_MAPPING = {
            "Factory": 0,
            "RetailChain": 1,
            "IndividualEntrepreneur": 2,
        }
        return HIERARCHY_MAPPING.get(self.role_type, -1)

    def clean(self):
        if not self.pk:
            return self.supplier
        parent = self.supplier
        while parent is not None:
            if parent == self:
                raise ValidationError("Creating this item would create a cycle")
            parent = parent.supplier
