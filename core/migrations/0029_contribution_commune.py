# Generated by Django 5.0.6 on 2024-05-23 09:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0028_digitalservice_ordre'),
    ]

    operations = [
        migrations.AddField(
            model_name='contribution',
            name='commune',
            field=models.CharField(max_length=500, null=True),
        ),
    ]
