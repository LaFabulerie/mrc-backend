# Generated by Django 5.0.6 on 2024-05-31 08:17

import autoslug.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parameters', '0002_alter_parameter_dec_value_alter_parameter_int_value_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='parameter',
            name='slug',
            field=autoslug.fields.AutoSlugField(always_update=True, default=None, editable=False, populate_from='name', unique=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='parameter',
            name='dec_value',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True),
        ),
        migrations.AlterField(
            model_name='parameter',
            name='int_value',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='parameter',
            name='str_value',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]
