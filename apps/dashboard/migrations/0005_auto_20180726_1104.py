# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-07-26 16:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0004_auto_20180726_1028'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='day',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='game',
            name='time',
            field=models.TimeField(),
        ),
    ]
