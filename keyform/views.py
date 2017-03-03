# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views.generic.list import ListView
from keyform.models import Request, Comment


class HomeView(ListView):
    model = Request
    template_name = "keyform/home.html"
    
