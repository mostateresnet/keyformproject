from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic import RedirectView
from django.contrib.auth.views import login, logout_then_login
from keyform import views

urlpatterns = [
    url(r'^$', views.HomeView.as_view(), name='home'),
    url(r'^table.php$', RedirectView.as_view(pattern_name='home', permanent=True)),
    url(r'^contact$', views.ContactView.as_view(), name='contact'),
    url(r'^edit-contact/(?P<pk>\d+)$', views.EditContactView.as_view(), name='edit-contact'),
    url(r'^create-contact$', views.NewContactView.as_view(), name='create-contact'),
    url(r'^edit-request/(?P<pk>\d+)$', views.RequestView.as_view(), name='edit-request'),
    url(r'^create$', views.KeyRequest.as_view(), name='create'),
    url(r'^add-comment$', views.RequestCommentView.as_view(), name='add-comment'),
    url(r'^login$', login, name='login', kwargs={'template_name': 'keyform/login.html'}),
    url(r'^logout$', logout_then_login, name='logout'),
]
