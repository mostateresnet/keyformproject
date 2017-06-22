# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
from django.views.generic import FormView, UpdateView, CreateView
from django.views.generic.list import ListView
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404
from django.db.models import Count
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.timezone import localtime
from keyform.forms import CreateForm, RequestFormSet, EditForm, AddCommentForm
from keyform.models import Request, Comment

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
    template_name = "keyform/request.html"
    form_class = EditForm

    def get_success_url(self):
        return reverse('home')

class RequestCommentView(CreateView):
    model = Comment
    form_class = AddCommentForm

    def get_success_url(self):
        return reverse('home')

    def post(self, request, *args, **kwargs):
        message = request.POST['message']
        pk = request.POST['pk']

        req = get_object_or_404(Request, pk=pk)
        comment = req.comment_set.create(message=message, author=request.user)

        timestamp = localtime(comment.created_timestamp).strftime('%B %d, %Y, %I:%M %p')

        return HttpResponse(json.dumps({'author': str(comment.author), 'timestamp': timestamp, 'message': comment.message}), content_type="application/json")

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
