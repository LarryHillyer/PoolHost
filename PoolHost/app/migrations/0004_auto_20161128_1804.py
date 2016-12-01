# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-29 01:04
from __future__ import unicode_literals

import app.mixins
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0003_auto_20161123_0944'),
    ]

    operations = [
        migrations.CreateModel(
            name='PoolOwner_Choices',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('poolowner', models.IntegerField()),
            ],
            bases=(models.Model, app.mixins.HelperMixins),
        ),
    ]