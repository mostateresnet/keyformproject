from django.conf.urls import url, include
from django.contrib import admin
from keyform import views

urlpatterns = [
    url(r'^$', views.HomeView.as_view(), name='home'),
    url(r'^edit-request/(?P<pk>\d+)$', views.RequestView.as_view(), name='edit-request'),
    url(r'^create$', views.KeyRequest.as_view(), name='create'),
    url(r'^add-comment$', views.RequestCommentView.as_view(), name='add-comment'),
]
