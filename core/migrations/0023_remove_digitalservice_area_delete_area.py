# Generated by Django 4.2.4 on 2023-10-14 07:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('org', '0008_remove_organization_area'),
        ('core', '0022_digitalservice_scope'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='digitalservice',
            name='area',
        ),
        migrations.DeleteModel(
            name='Area',
        ),
    ]
