# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic import CreateView
from keyform.forms import CreateForm
from keyform.models import Request

class HomeView(TemplateView):
	template_name = "keyform/home.html"

class NewForm(CreateView):
	template_name = "keyform/add_form.html"
	model = Request
	# fields = ['building', 'student_name', 'reason_for_request', 'amt_recieved', 'payment_method', 'charge_amount', 'staff', 'bpn', 'created_timestamp', 'charged_on_rcr']
	success_url = "/"

	def get_form_class(self):
		return CreateForm
