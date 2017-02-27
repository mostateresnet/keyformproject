# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from keyform import models
# Register your models here.
admin.site.register(models.Request)
admin.site.register(models.Building)
admin.site.register(models.KeyData)
admin.site.register(models.Comment)
