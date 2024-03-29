# Generated by Django 4.2.4 on 2023-10-14 07:10

from django.db import migrations, models


def populate_scope(apps, schema_editor):
    DigitalService = apps.get_model('core', 'DigitalService')
    for digital_service in DigitalService.objects.all():
        digital_service.scope = digital_service.area.name
        digital_service.save()

class Migration(migrations.Migration):

    dependencies = [
        ('core', '0021_digitalservice_contact_delete_digitalservicecontact'),
    ]

    operations = [
        migrations.AddField(
            model_name='digitalservice',
            name='scope',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.RunPython(populate_scope),
    ]
