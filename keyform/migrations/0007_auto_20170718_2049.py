# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-07-18 20:49
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('keyform', '0006_auto_20170621_0042'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=75)),
            ],
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
                ('order', models.IntegerField()),
            ],
            options={
                'verbose_name_plural': 'Statuses',
                'ordering': ['order'],
            },
        ),
        migrations.AlterModelOptions(
            name='building',
            options={'ordering': ['name']},
        ),
        migrations.AlterModelOptions(
            name='request',
            options={'ordering': ['-created_timestamp']},
        ),
        migrations.AddField(
            model_name='request',
            name='locksmith_email_sent',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='request',
            name='updated',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='keydata',
            name='core_number',
            field=models.CharField(max_length=35, verbose_name='New Core Number'),
        ),
        migrations.AlterField(
            model_name='keydata',
            name='key_number',
            field=models.CharField(max_length=24, verbose_name='Lost/Stolen Key Number'),
        ),
        migrations.AlterField(
            model_name='request',
            name='reason_for_request',
            field=models.CharField(choices=[('dk', 'Damaged Key'), ('lk', 'Lost/Stolen Key'), ('sk', 'Staff File Key')], max_length=2),
        ),
        migrations.AlterField(
            model_name='request',
            name='status',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='status', to='keyform.Status'),
        ),
        migrations.AddField(
            model_name='contact',
            name='alert_statuses',
            field=models.ManyToManyField(to='keyform.Status'),
        ),
        migrations.AddField(
            model_name='contact',
            name='buildings',
            field=models.ManyToManyField(to='keyform.Building'),
        ),
        migrations.AddField(
            model_name='request',
            name='previous_status',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='previous_status', to='keyform.Status'),
            preserve_default=False,
        ),
    ]
