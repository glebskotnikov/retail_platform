# Generated by Django 5.1.2 on 2024-10-23 04:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0002_remove_user_role"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="role_label",
            field=models.CharField(
                blank=True, max_length=255, null=True, verbose_name="role_label"
            ),
        ),
    ]
