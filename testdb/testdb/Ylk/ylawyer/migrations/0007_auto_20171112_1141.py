# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-12 03:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ylawyer', '0006_auto_20171112_1127'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useraddrlist',
            name='addr_id',
            field=models.AutoField(primary_key=True, serialize=False, verbose_name='地址id'),
        ),
        migrations.AlterField(
            model_name='useraddrlist',
            name='user_id',
            field=models.CharField(max_length=256, verbose_name='用户id'),
        ),
    ]
