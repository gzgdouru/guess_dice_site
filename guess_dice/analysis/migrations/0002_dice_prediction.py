# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-10-25 11:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analysis', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='dice',
            name='prediction',
            field=models.CharField(default='', max_length=16, verbose_name='预期'),
        ),
    ]
