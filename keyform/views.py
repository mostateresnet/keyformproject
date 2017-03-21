# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from keyform.models import Request

from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic import CreateView

class HomeView(TemplateView):
	template_name = "keyform/home.html"
