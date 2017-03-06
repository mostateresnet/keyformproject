from django.conf.urls import url, include
from django.contrib import admin
from keyform import views 

urlpatterns = [
    url(r'^$', views.HomeView.as_view()),
    url(r'^create_new', views.NewForm.as_view(), name='NewForm'),
]
