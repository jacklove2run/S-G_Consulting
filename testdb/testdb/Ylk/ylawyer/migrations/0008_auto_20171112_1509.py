# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-12 07:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ylawyer', '0007_auto_20171112_1141'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderlist',
            name='recipient_addr',
            field=models.CharField(default='', max_length=255, verbose_name='收件人地址'),
        ),
        migrations.AddField(
            model_name='orderlist',
            name='recipient_name',
            field=models.CharField(default='', max_length=255, verbose_name='收件人'),
        ),
        migrations.AddField(
            model_name='orderlist',
            name='recipient_phone',
            field=models.CharField(default='', max_length=15, verbose_name='收件人手机号'),
        ),
    ]
