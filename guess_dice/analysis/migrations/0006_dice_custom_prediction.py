# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-11-14 13:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analysis', '0005_auto_20181106_1522'),
    ]

    operations = [
        migrations.AddField(
            model_name='dice',
            name='custom_prediction',
            field=models.CharField(default='', max_length=16, verbose_name='自定义'),
        ),
    ]
