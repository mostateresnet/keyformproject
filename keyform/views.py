# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.views.generic import FormView, UpdateView, CreateView
from django.views.generic.list import ListView
from keyform.forms import CreateForm, RequestFormSet, EditForm
from keyform.models import Request
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin

class HomeView(LoginRequiredMixin, ListView):
    model = Request
    template_name = "keyform/home.html"

    def get_context_data(self):
        context = super(HomeView, self).get_context_data()
        context["request_types"] = Request.REQUEST_TYPES
        context["status_types"] = Request.STATUS_TYPES
        return context


class SearchView(LoginRequiredMixin, ListView):
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

class RequestView(LoginRequiredMixin, UpdateView):
    model = Request
    template_name = "keyform/request.html"
    form_class = EditForm

    def get_success_url(self):
        return reverse('home')

class KeyRequest(LoginRequiredMixin, FormView):
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
        form = CreateForm(instance=Request(staff=self.request.user), **self.get_form_kwargs())
        form.request_formset = RequestFormSet(**self.get_form_kwargs())
        return form
