# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-03 03:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ylawyer', '0003_auto_20171029_1444'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderlist',
            name='product_id',
            field=models.IntegerField(default='1', verbose_name='商品ID'),
        ),
    ]