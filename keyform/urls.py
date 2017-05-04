from django.conf.urls import url, include
from django.contrib import admin
from keyform import views

urlpatterns = [
    url(r'^search', views.SearchView.as_view(), name="search"),
    url(r'^$', views.HomeView.as_view(), name='home'),
    url(r'^create$', views.KeyRequest.as_view(), name='create')
]
