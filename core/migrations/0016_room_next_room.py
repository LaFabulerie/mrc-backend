# Generated by Django 4.2.4 on 2023-08-18 09:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0015_alter_room_options_alter_room_light_pin'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='next_room',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='previous_room', to='core.room', verbose_name='Pièce suivante'),
        ),
    ]