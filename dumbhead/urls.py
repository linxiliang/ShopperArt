"""Dumbhead urls."""
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^item$', views.item, name='item'),
    url(r'^search$', views.search, name='search'),
    url(r'^$', views.index, name='index'),
]
