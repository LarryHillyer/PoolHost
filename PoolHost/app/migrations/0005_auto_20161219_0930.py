# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-19 16:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_auto_20161219_0916'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nfl_schedule',
            name='cronjob_id',
            field=models.IntegerField(null=True),
        ),
    ]
