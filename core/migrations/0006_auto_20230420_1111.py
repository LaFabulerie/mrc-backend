# Generated by Django 4.1.7 on 2023-04-20 09:11

from django.db import migrations


import uuid

def gen_uuid(apps, schema_editor):
    models = ['DigitalService', 'DigitalUse', 'Item', 'Room']
    for model in models:
        Model = apps.get_model('core', model)
        for row in Model.objects.all():
            row.uuid = uuid.uuid4()
            row.save(update_fields=['uuid'])


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0005_digitalservice_uuid_digitaluse_uuid_item_uuid_and_more"),
    ]

    operations = [
        migrations.RunPython(gen_uuid, reverse_code=migrations.RunPython.noop),
    ]