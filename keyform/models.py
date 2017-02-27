# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from django.utils.timezone import now


class Request(models.Model):

    REQUEST_TYPES = (
        ('bk', 'Broken Key'),
        ('sk', 'Stolen Key'),
        ('wk', 'Worker Key'),
    )

    PAYMENT_TYPES = (
        ('ca', 'Cash'),
        ('ch', 'Check'),
    )

    building = models.ForeignKey('Building')
    student_name = models.CharField(max_length=128)
    reason_for_request = models.CharField(max_length=2, choices=REQUEST_TYPES)
    amt_recieved = models.DecimalField(max_digits=7, decimal_places=2, default=0, blank=True)
    paid_by = models.CharField(max_length=2, choices=PAYMENT_TYPES)
    charge_amount = models.DecimalField(max_digits=7, decimal_places=2)
    staff_name = models.ForeignKey(settings.AUTH_USER_MODEL)
    bpn = models.CharField(max_length=9)
    created_timestamp = models.DateTimeField(default=now, blank=True)
    charged_on_rcr = models.BooleanField(default=False)


class Building(models.Model):
    name = models.CharField(max_length=256)


class KeyData(models.Model):

    KEY_TYPES = (
        ('rm', 'Room/Apt.'),
        ('mb', 'Mailbox'),
        ('ot', 'Other (Specify)'),
    )

    request = models.ForeignKey(Request)
    new_core_number = models.CharField(max_length=35)
    key_type = models.CharField(max_length=2, choices=KEY_TYPES)
    room_number = models.CharField(max_length=42)
    lost_key_number = models.CharField(max_length=24)
    quantity = models.IntegerField()

    class Meta:
        verbose_name_plural = 'Key Data'


class Comment(models.Model):
    request = models.ForeignKey(Request)
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    created_timestamp = models.DateTimeField(default=now, blank=True)
    message = models.TextField()
