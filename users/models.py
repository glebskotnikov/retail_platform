from django.contrib.auth.models import AbstractUser
from django.db import models

NULLABLE = {"blank": True, "null": True}


class User(AbstractUser):
    username = None

    name = models.CharField(max_length=50, verbose_name="name")
    email = models.EmailField(unique=True, verbose_name="email")
    country = models.CharField(max_length=100, verbose_name="country", **NULLABLE)
    city = models.CharField(max_length=50, verbose_name="city", **NULLABLE)
    street = models.CharField(max_length=100, verbose_name="street", **NULLABLE)
    house_number = models.CharField(
        max_length=20, verbose_name="house_number", **NULLABLE
    )

    debt = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="debt", **NULLABLE
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="created_at")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"
        ordering = ["email"]

    def __str__(self):
        return self.email
