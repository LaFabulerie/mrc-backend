# Generated by Django 4.1.7 on 2023-04-19 07:55

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("client", "0002_alter_remoteaccess_api_key_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="remoteaccess",
            name="updated_at",
        ),
    ]