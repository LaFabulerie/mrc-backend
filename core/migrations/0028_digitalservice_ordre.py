# Generated by Django 5.0.6 on 2024-05-23 09:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0027_remove_contribution_tags_contribution_tags'),
    ]

    operations = [
        migrations.AddField(
            model_name='digitalservice',
            name='ordre',
            field=models.IntegerField(default=1),
        ),
    ]