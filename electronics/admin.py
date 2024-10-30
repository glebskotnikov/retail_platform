from django.contrib import admin

from .models import Product, Role


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ("user", "role_type", "supplier")


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "model", "release_date")
