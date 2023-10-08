# Generated by Django 4.2.4 on 2023-10-07 14:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feedback', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='feedback',
            options={'ordering': ('-created_at',)},
        ),
        migrations.AlterModelOptions(
            name='question',
            options={'ordering': ('order',)},
        ),
        migrations.AddField(
            model_name='question',
            name='allow_comment',
            field=models.BooleanField(default=False),
        ),
    ]
