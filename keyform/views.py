# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.views.generic.base import TemplateView
from django.views.generic import FormView, UpdateView, CreateView
from django.views.generic.list import ListView
from keyform.forms import CreateForm, RequestFormSet, EditForm, ContactForm
from keyform.models import Request, Building, Contact
from django.urls import reverse_lazy
from django.forms import modelformset_factory
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models import Count

class HomeView(LoginRequiredMixin, ListView):
    model = Request
    template_name = "keyform/home.html"
    paginate_by = 25

    def get_queryset(self):
        q_set = super(HomeView, self).get_queryset()
        q_set = q_set.select_related('building')
        q_set = q_set.prefetch_related('keydata_set')
        q_set = q_set.annotate(num_comments=Count('comment'))
        return q_set


class RequestView(LoginRequiredMixin, UpdateView):
    model = Request
    success_url = reverse_lazy('home')
    template_name = "keyform/request.html"
    form_class = EditForm


class ContactView(LoginRequiredMixin, TemplateView):
    template_name = "keyform/contact.html"

    def get_context_data(self):
        context = super(ContactView, self).get_context_data()
        context["buildings"] = Building.objects.all()
        return context

    def post(self, request, *args, **kwargs):

        success = False
        if request.user.has_perm('keyform.delete_contact'):
            pk = request.POST['pk']
            Contact.objects.filter(pk=pk).delete();
            success = True

        return JsonResponse({'success': success})

class EditContactView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    template_name = "keyform/contact_form.html"
    model = Contact
    form_class = ContactForm
    success_url = reverse_lazy('contact')
    permission_required = 'keyform.change_contact'
    raise_exception = True


class NewContactView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    template_name = "keyform/contact_form.html"
    model = Contact
    form_class = ContactForm
    success_url = reverse_lazy('contact')


    permission_required = 'keyform.add_contact'
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
