# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-07-26 16:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0005_auto_20180726_1104'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='game_system',
            field=models.CharField(blank=True, default='', max_length=64),
        ),
    ]
