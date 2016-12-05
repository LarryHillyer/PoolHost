# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-01 21:36
from __future__ import unicode_literals

import app.mixins
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0006_auto_20161130_1825'),
    ]

    operations = [
        migrations.CreateModel(
            name='CronJob_Choices',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('cronjob_id', models.IntegerField()),
            ],
            bases=(models.Model, app.mixins.HelperMixins),
        ),
        migrations.CreateModel(
            name='PoolType_Choices',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('pooltype_id', models.IntegerField()),
            ],
            bases=(models.Model, app.mixins.HelperMixins),
        ),
    ]