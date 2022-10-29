# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='IgnoredURL',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('pattern', models.CharField(max_length=255)),
                ('description', models.CharField(help_text=b'What this URL pattern covers.', max_length=75)),
            ],
        ),
        migrations.CreateModel(
            name='Maintenance',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_being_performed', models.BooleanField(default=False, verbose_name=b'In Maintenance Mode')),
                ('site', models.ForeignKey(to='sites.Site', on_delete=models.CASCADE)),
            ],
            options={
                'verbose_name': 'Maintenance Mode',
                'verbose_name_plural': 'Maintenance Mode',
            },
        ),
        migrations.AddField(
            model_name='ignoredurl',
            name='maintenance',
            field=models.ForeignKey(to='maintenancemode.Maintenance', on_delete=models.CASCADE),
        ),
    ]
