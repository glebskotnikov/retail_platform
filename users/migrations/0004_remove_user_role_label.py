# Generated by Django 5.1.2 on 2024-10-23 20:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0003_user_role_label"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="user",
            name="role_label",
        ),
    ]