# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.views.generic import ListView, UpdateView, CreateView
from django.views.generic.list import ListView
from keyform.forms import CreateForm, EditForm
from keyform.models import Request
from django.urls import reverse_lazy, reverse

class HomeView(ListView):
    model = Request
    template_name = "keyform/home.html"

class RequestView(UpdateView):
    model = Request
    template_name = "keyform/request.html"
    fields = ['status']

    def get_success_url(self):
        return reverse('home')

class NewForm(CreateView):
    template_name = "keyform/add_form.html"
    model = Request
    success_url = reverse_lazy('home')
    form_class = CreateForm
