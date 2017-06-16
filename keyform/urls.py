from django.conf.urls import url, include
from django.contrib import admin
from keyform import views

urlpatterns = [
    url(r'^$', views.HomeView.as_view(), name='home'),
    url(r'^contact', views.ContactView.as_view(), name='contact'),
    url(r'^edit-contact/(?P<pk>\d+)$', views.EditContactView.as_view(), name='edit_contact'),
    url(r'^create-contact', views.NewContactView.as_view(), name='create_contact'),
    url(r'^edit-request/(?P<pk>\d+)$', views.RequestView.as_view(), name='edit-request'),
    url(r'^create$', views.KeyRequest.as_view(), name='create')
]
