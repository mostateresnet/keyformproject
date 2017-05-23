from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth.views import login, logout_then_login
from keyform import views

urlpatterns = [
    url(r'^$', views.HomeView.as_view(), name='home'),
    url(r'^edit-request/(?P<pk>\d+)$', views.RequestView.as_view(), name='edit-request'),
    url(r'^create$', views.KeyRequest.as_view(), name='create'),
    url(r'^login$', login, name='login', kwargs={'template_name': 'keyform/login.html'}),
    url(r'^logout$', logout_then_login, name='logout')
]
