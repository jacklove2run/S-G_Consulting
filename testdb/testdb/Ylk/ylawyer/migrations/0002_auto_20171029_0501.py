# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-29 05:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ylawyer', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderlist',
            name='product_price',
            field=models.FloatField(verbose_name='商品价格'),
        ),
        migrations.AlterField(
            model_name='productinfo',
            name='product_price',
            field=models.FloatField(verbose_name='商品价格'),
        ),
    ]