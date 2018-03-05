# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from keyform import models

class BuildingAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        return models.Building.all_buildings.all()

admin.site.register(models.Request)
admin.site.register(models.Building, BuildingAdmin)
admin.site.register(models.KeyData)
admin.site.register(models.Comment)
admin.site.register(models.Contact)
admin.site.register(models.Status)
admin.site.register(models.KeyType)
