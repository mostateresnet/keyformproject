# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-07-27 18:39
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('keyform', '0007_auto_20170718_2049'),
    ]

    operations = [
        migrations.AlterField(
            model_name='request',
            name='bpn',
            field=models.CharField(blank=True, max_length=9, validators=[django.core.validators.RegexValidator('[mM8]\\d{8}', "Bearpass number must start with an 'M,' 'm,' or '8,' and followed by eight digits.")], verbose_name='M-Number'),
        ),
    ]
