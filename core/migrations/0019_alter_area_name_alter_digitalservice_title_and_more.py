# Generated by Django 4.2.4 on 2023-10-08 09:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0018_remove_room_light_pin'),
    ]

    operations = [
        migrations.AlterField(
            model_name='area',
            name='name',
            field=models.CharField(max_length=500),
        ),
        migrations.AlterField(
            model_name='digitalservice',
            name='title',
            field=models.CharField(max_length=500),
        ),
        migrations.AlterField(
            model_name='digitaluse',
            name='title',
            field=models.CharField(max_length=500),
        ),
        migrations.AlterField(
            model_name='item',
            name='image',
            field=models.CharField(blank=True, editable=False, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='item',
            name='name',
            field=models.CharField(max_length=500, verbose_name='Nom'),
        ),
        migrations.AlterField(
            model_name='room',
            name='video',
            field=models.CharField(blank=True, editable=False, max_length=500, null=True),
        ),
    ]
