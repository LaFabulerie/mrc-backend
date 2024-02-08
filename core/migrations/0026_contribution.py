# Generated by Django 5.0.1 on 2024-02-08 13:44

import django.db.models.deletion
import taggit.managers
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0025_alter_room_options_remove_room_position'),
        ('taggit', '0006_rename_taggeditem_content_type_object_id_taggit_tagg_content_8fc721_idx'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contribution',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('usage_title', models.CharField(blank=True, max_length=500, null=True)),
                ('title', models.CharField(max_length=500)),
                ('description', models.TextField(blank=True, null=True)),
                ('url', models.CharField(max_length=500)),
                ('scope', models.CharField(max_length=500)),
                ('contact', models.TextField(blank=True, null=True)),
                ('item', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='contributions', to='core.item')),
                ('tags', taggit.managers.TaggableManager(blank=True, help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags')),
                ('use', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='contributions', to='core.digitaluse')),
            ],
            options={
                'verbose_name': 'Contribution',
                'verbose_name_plural': 'Contributions',
            },
        ),
    ]
