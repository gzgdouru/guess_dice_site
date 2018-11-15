# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-11-15 10:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analysis', '0008_auto_20181115_0953'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dice',
            name='custom_balance',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=13, verbose_name='自定义余额'),
        ),
        migrations.AlterField(
            model_name='dice',
            name='eleven_balance',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=13, verbose_name='十一期余额'),
        ),
        migrations.AlterField(
            model_name='dice',
            name='five_balance',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=13, verbose_name='五期余额'),
        ),
        migrations.AlterField(
            model_name='dice',
            name='nine_balance',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=13, verbose_name='九期余额'),
        ),
        migrations.AlterField(
            model_name='dice',
            name='seven_balance',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=13, verbose_name='七期余额'),
        ),
        migrations.AlterField(
            model_name='dice',
            name='three_balance',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=13, verbose_name='三期余额'),
        ),
    ]