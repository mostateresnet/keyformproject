# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.views.generic import ListView, UpdateView
from keyform.models import Request


class HomeView(ListView):
    model = Request
    template_name = "keyform/home.html"

class RequestView(UpdateView):
    model = Request
    template_name = "keyform/request.html"
    fields = ['student_name']
