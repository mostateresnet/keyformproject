# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.views.generic import FormView
from django.views.generic.list import ListView
from keyform.forms import CreateForm, RequestFormSet
from keyform.models import Request
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.db.models import Count
from django.core.paginator import Paginator

class HomeView(ListView):
    model = Request
    template_name = "keyform/home.html"
    paginate_by = 25

    def get_queryset(self):
        q_set = super(HomeView, self).get_queryset()
        q_set = q_set.select_related('building')
        q_set = q_set.prefetch_related('keydata_set')
        q_set = q_set.annotate(num_comments=Count('comment'))
        return q_set


class KeyRequest(FormView):
    template_name = "keyform/add_form.html"
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        new_request = form.save(commit=False)
        form.request_formset = RequestFormSet(self.request.POST, instance=new_request)
        for request_form in form.request_formset.forms:
            request_form.empty_permitted = False
        if form.request_formset.is_valid() and form.request_formset.has_changed():
            new_request.save()
            form.request_formset.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.form_invalid(form)

    def get_form(self, form_class=None):
        form = CreateForm(**self.get_form_kwargs())
        form.request_formset = RequestFormSet(**self.get_form_kwargs())
        return form
