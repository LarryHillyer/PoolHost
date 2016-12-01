# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-01 01:25
from __future__ import unicode_literals

import app.mixins
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0005_auto_20161128_1925'),
    ]

    operations = [
        migrations.CreateModel(
            name='CronJobType_Choices',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('cronjobtype_id', models.IntegerField()),
            ],
            bases=(models.Model, app.mixins.HelperMixins),
        ),
    ]
