# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-12 03:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ylawyer', '0005_auto_20171111_1423'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='user_id',
            field=models.CharField(max_length=155, verbose_name='用户id'),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='user_wechat_name',
            field=models.CharField(default='', max_length=155, verbose_name='用户微信昵称'),
        ),
    ]
