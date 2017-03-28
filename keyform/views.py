# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.views.generic import CreateView
from django.views.generic.list import ListView
from keyform.forms import CreateForm
from keyform.models import Request

class HomeView(ListView):
    model = Request
    template_name = "keyform/home.html"

class NewForm(CreateView):
    template_name = "keyform/add_form.html"
    model = Request
    success_url = "/"
    form_class = CreateForm
