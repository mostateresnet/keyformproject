# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _
from django.core.validators import MinValueValidator
from decimal import Decimal
from django.core.validators import RegexValidator

class Building(models.Model):
    name = models.CharField(max_length=256)

    def __str__(self):
        return self.name


class Request(models.Model):

    REQUEST_TYPES = (
        ('bk', _('Broken Key')),
        ('sk', _('Stolen Key')),
        ('wk', _('Worker Key')),
    )

    PAYMENT_TYPES = (
        ('ca', _('Cash')),
        ('ch', _('Check')),
    )

    STATUS_TYPES = (
        ('pr', _('Processing')),
        ('ks', _('Key Sent')),
        ('kd', _('Key Distributed')),
    )

    bpn_validator = RegexValidator('[mM8]\d{8}', "Bearpass number must start with an 'M,' 'm,' or '8,' and followed by eight digits.'")

    building = models.ForeignKey(Building)
    student_name = models.CharField(max_length=128, blank=True)
    reason_for_request = models.CharField(max_length=2, choices=REQUEST_TYPES)
    amt_received = models.DecimalField(max_digits=7, decimal_places=2, default=0, blank=True, verbose_name= _('Amount received'), validators=[MinValueValidator(Decimal('0.00'))])
    payment_method = models.CharField(max_length=2, choices=PAYMENT_TYPES, null=True, blank=True)
    charge_amount = models.DecimalField(max_digits=7, decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))])
    staff = models.ForeignKey(settings.AUTH_USER_MODEL)
    bpn = models.CharField(max_length=9, verbose_name=_('M-Number'), validators=[bpn_validator])
    created_timestamp = models.DateTimeField(default=now, blank=True)
    charged_on_rcr = models.BooleanField(default=False, verbose_name=_('Charged on RCR'))
    status = models.CharField(max_length=2, choices=STATUS_TYPES, default = 'pr')

    def __str__(self):
        return str(self.get_reason_for_request_display()) + " " + str(self.created_timestamp)

    class Meta:
        ordering = ['-created_timestamp']


class KeyData(models.Model):

    KEY_TYPES = (
        ('rm', _('Room/Apt.')),
        ('mb', _('Mailbox')),
        ('ot', _('Other (Specify)')),
    )

    request = models.ForeignKey(Request)
    core_number = models.CharField(max_length=35)
    key_type = models.CharField(max_length=2, choices=KEY_TYPES)
    room_number = models.CharField(max_length=42)
    key_number = models.CharField(max_length=24)
    quantity = models.IntegerField()

    def __str__(self):
        return str(self.core_number)

    class Meta:
        verbose_name_plural = _('Key Data')


class Comment(models.Model):
    request = models.ForeignKey(Request)
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    created_timestamp = models.DateTimeField(default=now, blank=True)
    message = models.TextField()

    class Meta:
        ordering = ['created_timestamp']

    def __str__(self):
        return str(self.created_timestamp)
