# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-10-24 11:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Dice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('period', models.CharField(max_length=32, verbose_name='周期')),
                ('num_1', models.PositiveIntegerField(verbose_name='数字1')),
                ('num_2', models.PositiveIntegerField(verbose_name='数字2')),
                ('num_3', models.PositiveIntegerField(verbose_name='数字3')),
                ('add_time', models.DateTimeField(auto_now_add=True, verbose_name='添加时间')),
            ],
            options={
                'db_table': 'tb_guess_dice',
            },
        ),
    ]
