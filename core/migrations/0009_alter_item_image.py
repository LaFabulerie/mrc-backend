# Generated by Django 4.2.1 on 2023-07-17 07:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_room_main_color'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='image',
            field=models.FileField(blank=True, null=True, upload_to='images'),
        ),
    ]
