# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-15 16:22
from __future__ import unicode_literals

from decimal import Decimal
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('keyform', '0003_merge_20170324_1622'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='request',
            name='amt_recieved',
        ),
        migrations.AddField(
            model_name='request',
            name='amt_received',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=7, validators=[django.core.validators.MinValueValidator(Decimal('0.00'))], verbose_name='Amount received'),
        ),
        migrations.AlterField(
            model_name='request',
            name='bpn',
            field=models.CharField(max_length=9, validators=[django.core.validators.RegexValidator('[mM8]\\d{8}', "Bearpass number must start with an 'M,' 'm,' or '8,' and followed by eight digits.'")], verbose_name='M-Number'),
        ),
        migrations.AlterField(
            model_name='request',
            name='charge_amount',
            field=models.DecimalField(decimal_places=2, max_digits=7, validators=[django.core.validators.MinValueValidator(Decimal('0.00'))]),
        ),
        migrations.AlterField(
            model_name='request',
            name='charged_on_rcr',
            field=models.BooleanField(default=False, verbose_name='Charged on RCR'),
        ),
    ]
