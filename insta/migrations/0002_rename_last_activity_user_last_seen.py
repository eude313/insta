# Generated by Django 5.0.1 on 2024-01-30 23:37

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("insta", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="user",
            old_name="last_activity",
            new_name="last_seen",
        ),
    ]
