# Generated by Django 4.1.7 on 2023-04-19 13:09

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("client", "0003_remove_remoteaccess_updated_at"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="remoteaccess",
            options={
                "verbose_name": "Accès distant",
                "verbose_name_plural": "Accès distants",
            },
        ),
    ]