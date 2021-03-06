# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.core.validators import MinValueValidator
from decimal import Decimal
from django.core.validators import RegexValidator

class BuildingManager(models.Manager):
    def get_queryset(self):
        return super(BuildingManager, self).get_queryset().filter(deleted=False)

class Building(models.Model):
    name = models.CharField(max_length=256)
    deleted = models.BooleanField(default=False)
    objects = BuildingManager()
    all_buildings = models.Manager()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

class Status(models.Model):

    name = models.CharField(max_length=32)
    order = models.IntegerField()
    visible = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = _('Statuses')
        ordering = ['order']

class RequestManager(models.Manager):
    def get_queryset(self):
        return super(RequestManager, self).get_queryset().filter(status__visible=True)

class Request(models.Model):

    REQUEST_TYPES = (
        ('dk', _('Damaged Key')),
        ('lk', _('Lost/Stolen Key')),
        ('sk', _('Staff File Key')),
    )

    PAYMENT_TYPES = (
        ('ca', _('Cash')),
        ('ch', _('Check')),
        ('na', _('Not Applicable')),
    )

    objects = models.Manager()
    active_objects = RequestManager()

    bpn_validator = RegexValidator('[mM8]\d{8}', _("Bearpass number must start with an 'M,' 'm,' or '8,' and followed by eight digits."))

    building = models.ForeignKey(Building)
    student_name = models.CharField(max_length=128, blank=True)
    reason_for_request = models.CharField(max_length=2, choices=REQUEST_TYPES, verbose_name=_("Request for:"))
    amt_received = models.DecimalField(max_digits=7, decimal_places=2, default=0, blank=True, verbose_name= _('Amount received'), validators=[MinValueValidator(Decimal('0.00'))],
        help_text=_('Core Change/Reprogram Fob Charge = $50, Room Key/Fob = $10, Mailbox Key = $10, Monroe Mailbox Key = $25'))
    payment_method = models.CharField(max_length=2, choices=PAYMENT_TYPES)
    charge_amount = models.DecimalField(max_digits=7, default=0, decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))], verbose_name=_("Bill to Account:"))
    staff = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('Staff member completing request'))
    bpn = models.CharField(max_length=9, verbose_name=_('M-Number'), validators=[bpn_validator], blank=True)
    created_timestamp = models.DateTimeField(default=now, blank=True)
    charged_on_rcr = models.BooleanField(default=False, verbose_name=_('Charged on RCR'))
    status = models.ForeignKey(Status, related_name="status")
    previous_status = models.ForeignKey(Status, related_name="previous_status")
    locksmith_email_sent = models.BooleanField(default=False)
    updated = models.BooleanField(default=True)

    def core_number_list(self):
        return [kd.core_number for kd in self.keydata_set.all() if kd.core_number]

    def room_number_list(self):
        return [kd.room_number for kd in self.keydata_set.all() if kd.room_number]

    def __str__(self):
        return str(self.get_reason_for_request_display()) + " " + str(self.created_timestamp)

    class Meta:
        ordering = ['-created_timestamp']

class KeyType(models.Model):
    name = models.CharField(max_length=128)
    hide_core_number = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class KeyData(models.Model):
    request = models.ForeignKey(Request)
    core_number = models.CharField(max_length=35, verbose_name=_('New Core Number'), blank=True,
        help_text=_('Use a comma to separate the list of cores (if suite style).'))
    key_type = models.ForeignKey(KeyType, null=True)
    room_number = models.CharField(max_length=42)
    key_number = models.CharField(max_length=24, verbose_name=_('Lost/Stolen/Damaged Key Number'))
    quantity = models.IntegerField(validators=[MinValueValidator(0)],
        help_text=_("If you don't need to order more keys because there are enough already, you can mark zero."))

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


class Contact(models.Model):
    buildings = models.ManyToManyField(Building)
    alert_statuses = models.ManyToManyField(Status)
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=75, unique=True)


    def __str__(self):
        return self.name


@receiver(pre_save, sender=Request)
def handle(sender, instance, **kwargs):
    request = Request.objects.filter(pk=instance.pk).first()
    if request is not None:
        if instance.status != request.status:
            instance.previous_status = request.status
            instance.updated = False
    else:
        instance.previous_status = instance.status
