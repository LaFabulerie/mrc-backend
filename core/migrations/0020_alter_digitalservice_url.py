# Generated by Django 4.2.4 on 2023-10-08 09:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0019_alter_area_name_alter_digitalservice_title_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='digitalservice',
            name='url',
            field=models.URLField(blank=True, max_length=500, null=True),
        ),
    ]
