# Generated by Django 4.2.4 on 2023-10-29 10:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0024_alter_digitalservice_url'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='room',
            options={'verbose_name': 'Pièce'},
        ),
        migrations.RemoveField(
            model_name='room',
            name='position',
        ),
    ]
