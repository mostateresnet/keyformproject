# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-08-11 20:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('keyform', '0008_status_visible'),
    ]

    operations = [
        migrations.AddField(
            model_name='building',
            name='deleted',
            field=models.BooleanField(default=False),
        ),
    ]
