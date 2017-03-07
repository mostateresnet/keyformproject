from django.conf.urls import url, include
from django.contrib import admin
from keyform import views
from django.conf import settings
import debug_toolbar

urlpatterns = [
    url(r'^$', views.HomeView.as_view()),
]
