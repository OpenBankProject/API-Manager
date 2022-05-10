# -*- coding: utf-8 -*-
"""
URLs for consumers app
"""

from django.conf.urls import url

from .views import IndexView, DetailView, EnableView, DisableView

urlpatterns = [
    url(r'^$',
        IndexView.as_view(),
        name='consumers-index'),
    url(r'^(?P<consumer_id>[0-9a-z\-]+)$',
        DetailView.as_view(),
        name='consumers-detail'),
    url(r'^(?P<consumer_id>[0-9a-z\-]+)/enable$',
        EnableView.as_view(),
        name='consumers-enable'),
    url(r'^(?P<consumer_id>[0-9a-z\-]+)/disable$',
        DisableView.as_view(),
        name='consumers-disable'),
]
