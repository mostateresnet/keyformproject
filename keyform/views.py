# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import datetime, timedelta
from django.views.generic import FormView, UpdateView, View, CreateView
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404
from django.db.models import Count
from django.utils.timezone import localtime, utc
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.utils.timezone import localtime, utc
from django.utils.dateparse import parse_date
from django.utils.translation import ugettext_lazy as _
from keyform.forms import CreateForm, RequestFormSet, EditForm, ContactForm
from keyform.models import Request, Building, Contact, Status


class HomeView(LoginRequiredMixin, ListView):
    queryset = Request.active_objects
    template_name = "keyform/home.html"
    paginate_by = 25
    valid_params = ['amt_recieved', 'bpn', 'building__name', 'building_id', 'charge_amount', 'charged_on_rcr',
                    'comment', 'created_timestamp', 'id', 'keydata__room_number', 'keydata__core_number', 'keydata__key_number',
                    'payment_method', 'reason_for_request', 'status', 'student_name', 'staff']

    def get_ordering(self):
        self.order = self.request.GET.get('order') or '-created_timestamp'
        return [self.order, '-created_timestamp']

    def get_context_data(self):
        context = super(HomeView, self).get_context_data()
        context["request_types"] = Request.REQUEST_TYPES
        context["requests"] = Request.objects.all()
        context["status_types"] = Status.objects.all()
        context["buildings"] = Building.objects.all()
        data = self.request.GET.copy()
        for k, v in self.request.GET.items():
            if k not in self.valid_params or not v:
                del data[k]
        data["start_date"] = self.request.GET.get('start_date', '')
        if data["start_date"] == '':
            del data["start_date"]
        data["end_date"] = self.request.GET.get('end_date', '')
        if data["end_date"] == '':
            del data["end_date"]

        context["search_data"] = data
        context["order"] = self.order
        context["order_desc"] = self.order[0] == '-'
        context["order_codename"] = self.order[1:] if context["order_desc"] else self.order
        return context

    def get_date_range(self):
        self.converted_start_date = parse_date(self.request.GET.get('start_date', '')) or datetime.min.replace(tzinfo=utc)
        self.converted_end_date = parse_date(self.request.GET.get('end_date', '')) or datetime.max.replace(tzinfo=utc)

        if self.converted_end_date != datetime.max.replace(tzinfo=utc):
            self.converted_end_date += timedelta(days=1)

    def get_queryset(self):
        qset = super(HomeView, self).get_queryset()
        qset = qset.select_related('building')
        qset = qset.prefetch_related('keydata_set')
        qset = qset.select_related('status')
        qset = qset.annotate(num_comments=Count('comment'))

        for item, value in self.request.GET.items():
            if str(item) in self.valid_params and str(item) != 'staff':
                if value != '':
                    qset = qset.filter(**{item + '__icontains': value})

        self.get_date_range()
        qset = qset.filter(created_timestamp__range=[self.converted_start_date, self.converted_end_date])

        staff_searched = self.request.GET.get('staff', '').split()

        filter_Qs = Q()
        for token in staff_searched:
            or_Qs = Q()
            for field in ['first_name', 'last_name', 'username', 'email']:
                or_Qs |= Q(**{'staff__' + field + '__icontains': token})
            filter_Qs &= or_Qs

        qset = qset.filter(filter_Qs)

        return qset


class RequestView(LoginRequiredMixin, UpdateView):
    model = Request
    success_url = reverse_lazy('home')
    template_name = "keyform/request.html"
    form_class = EditForm
    success_url = reverse_lazy("home")


class RequestCommentView(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        message = request.POST['message']
        pk = request.POST['pk']

        req = get_object_or_404(Request, pk=pk)
        comment = req.comment_set.create(message=message, author=request.user)

        timestamp = localtime(comment.created_timestamp).strftime('%B %d, %Y, %I:%M %p')
        return JsonResponse({'author': str(comment.author), 'timestamp': timestamp, 'message': comment.message})


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
            Contact.objects.filter(pk=pk).delete()
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
    comment_errors = []

    def form_valid(self, form):
        new_request = form.save(commit=False)
        form.request_formset = RequestFormSet(self.request.POST, instance=new_request)
        for request_form in form.request_formset.forms:
            request_form.empty_permitted = False
        if form.request_formset.is_valid() and form.request_formset.has_changed():
            comment_text = self.check_comment(form) # This will generate any self.comment_errors for us
            if self.comment_errors:
                return self.form_invalid(form)
            new_request.save()
            form.request_formset.save()
            if comment_text: # Create the comment AFTER saving new_request
                new_request.comment_set.create(message=comment_text, author=self.request.user)
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.form_invalid(form)

    def form_invalid(self, form):
        # Generate any self.comment_errors
        self.check_comment(form)
        return super(KeyRequest, self).form_invalid(form)

    def check_comment(self, form):
        comment_text = self.request.POST.get('comment_text', '')
        if comment_text.strip():
            return comment_text
        elif form.instance.reason_for_request in ("dk", "sk"):
            self.comment_errors = [_("This field is required.")]
        return ''

    def get_form(self, form_class=None):
        form = CreateForm(instance=Request(staff=self.request.user, status=Status.objects.first()), **self.get_form_kwargs())
        form.request_formset = RequestFormSet(**self.get_form_kwargs())
        return form

    def get_context_data(self, **kwargs):
        context = super(KeyRequest, self).get_context_data(**kwargs)
        if self.request.method == 'POST':
            context['comment_errors'] = self.comment_errors
            context['comment_text'] = self.request.POST.get('comment_text', '')
        return context
