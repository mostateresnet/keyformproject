# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2018-03-04 20:02
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('keyform', '0014_auto_20180110_2127'),
    ]

    operations = [
        migrations.AlterField(
            model_name='keydata',
            name='key_type',
            field=models.CharField(choices=[('rm', 'Room/Apt.'), ('mb', 'Mailbox'), ('ot', 'Other (Specify)')], max_length=2, default='ot', null=True),
            preserve_default=False,
        ),
        migrations.RemoveField(
            model_name='keydata',
            name='key_type',
        ),
        migrations.RenameField(
            model_name='keydata',
            old_name='new_key_type',
            new_name='key_type',
        ),
    ]
