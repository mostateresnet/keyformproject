# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2018-01-10 21:27
from __future__ import unicode_literals

from django.db import migrations


def forwards(apps, schema_editor):
    KeyData = apps.get_model("keyform", "KeyData")
    KeyType = apps.get_model("keyform", "KeyType")

    for old_key_type in KeyData._meta.get_field('key_type').flatchoices:
        new_key_type = KeyType.objects.create(name=old_key_type[1])
        KeyData.objects.filter(key_type=old_key_type[0]).update(new_key_type=new_key_type)

def backwards(apps, schema_editor):
    KeyData = apps.get_model("keyform", "KeyData")
    KeyType = apps.get_model("keyform", "KeyType")

    for old_key_type in KeyData._meta.get_field('key_type').flatchoices:
        KeyData.objects.filter(new_key_type__name=old_key_type[1]).update(key_type=old_key_type[0])



class Migration(migrations.Migration):

    dependencies = [
        ('keyform', '0013_auto_20180110_2122'),
    ]

    operations = [
        migrations.RunPython(forwards, backwards, hints={'target_db': 'default'}),
    ]
