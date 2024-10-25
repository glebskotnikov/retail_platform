# Generated by Django 5.1.2 on 2024-10-24 05:45

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("electronics", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="individualentrepreneur",
            name="role_ptr",
        ),
        migrations.RemoveField(
            model_name="retailchain",
            name="role_ptr",
        ),
        migrations.AlterModelOptions(
            name="role",
            options={
                "ordering": ["user"],
                "verbose_name": "Role",
                "verbose_name_plural": "Roles",
            },
        ),
        migrations.AddField(
            model_name="role",
            name="role_type",
            field=models.CharField(
                choices=[
                    ("Factory", "Factory"),
                    ("RetailChain", "Retail Chain"),
                    ("IndividualEntrepreneur", "Individual Entrepreneur"),
                ],
                default="Factory",
                max_length=30,
                verbose_name="role type",
            ),
        ),
        migrations.AddField(
            model_name="role",
            name="supplier",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="suppliers",
                to="electronics.role",
                verbose_name="supplier",
            ),
        ),
        migrations.DeleteModel(
            name="Factory",
        ),
        migrations.DeleteModel(
            name="IndividualEntrepreneur",
        ),
        migrations.DeleteModel(
            name="RetailChain",
        ),
    ]