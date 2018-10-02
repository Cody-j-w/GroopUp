# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-07-26 01:04
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('game_type', models.CharField(max_length=64)),
                ('status', models.CharField(max_length=10)),
                ('time', models.DateTimeField()),
                ('day', models.DateTimeField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='avatar',
            field=models.ImageField(default='', upload_to=''),
        ),
        migrations.AddField(
            model_name='user',
            name='description',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.CharField(default='', max_length=64),
        ),
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.CharField(default='', max_length=250),
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(default='', max_length=64),
        ),
        migrations.AddField(
            model_name='game',
            name='game_master',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='my_games', to='dashboard.User'),
        ),
        migrations.AddField(
            model_name='game',
            name='players',
            field=models.ManyToManyField(related_name='games', to='dashboard.User'),
        ),
    ]