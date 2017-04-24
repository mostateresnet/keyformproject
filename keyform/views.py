# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.views.generic import CreateView
from django.views.generic.list import ListView
from keyform.forms import CreateForm, RequestFormSet
from keyform.models import Request
from django.urls import reverse_lazy
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

class HomeView(ListView):
    model = Request
    template_name = "keyform/home.html"

def key_request(request):
    if request.POST:
        form = CreateForm(request.POST)
        if form.is_valid():
            create_new = form.save(commit=False)
            key_formset = RequestFormSet(request.POST, instance=create_new)
            if key_formset.is_valid():
                create_new.save()
                key_formset.save()
                return HttpResponseRedirect(reverse('home'))
    else:
        form = CreateForm()
        key_formset = RequestFormSet(instance=Request())
    return render(request, "keyform/add_form.html", {
        "form": form,
        "keydata_formset": key_formset,
    })
