# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.views.generic.list import ListView
from keyform.models import Request


class HomeView(ListView):
    model = Request
    template_name = "keyform/home.html"

    def get_context_data(self):
        context = super(HomeView, self).get_context_data()
        context["request_types"] = Request.REQUEST_TYPES
        context["status_types"] = Request.STATUS_TYPES
        return context



class SearchView(ListView):
    template_name = "keyform/home.html"

    def get_queryset(self):
        qset = Request.objects.all()
        valid = ['amt_recieved', 'bpn', 'building', 'building_id', 'charge_amount', 'charged_on_rcr',
                 'comment', 'created_timestamp', 'id', 'keydata__room_number', 'keydata__core_number', 'keydata__key_number',
                 'payment_method', 'reason_for_request', 'staff', 'staff_id', 'status', 'student_name']

        for item, value in self.request.GET.items():
            if str(item) in valid:
                if value != '':
                    qset = qset.filter(**{item + '__icontains': value})
        return qset

    def get_context_data(self):
        context = super(SearchView, self).get_context_data()
        context["request_types"] = Request.REQUEST_TYPES
        context["status_types"] = Request.STATUS_TYPES
        return context
