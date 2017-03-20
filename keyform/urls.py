from django.conf.urls import url, include
from django.contrib import admin
from keyform import views

urlpatterns = [
    url(r'^$', views.HomeView.as_view()),
    url(r'^search', views.SearchView.as_view(), name = "search"),
]
