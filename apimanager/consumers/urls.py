# -*- coding: utf-8 -*-
"""
URLs for consumers app
"""

from django.urls import re_path

from .views import IndexView, DetailView, EnableView, DisableView, UsageDataAjaxView

urlpatterns = [
    re_path(r'^$',
        IndexView.as_view(),
        name='consumers-index'),
    re_path(r'^(?P<consumer_id>[0-9a-zA-Z\-_(){}%]+)$',
        DetailView.as_view(),
        name='consumers-detail'),
    re_path(r'^(?P<consumer_id>[0-9a-zA-Z\-_(){}%]+)/enable$',
        EnableView.as_view(),
        name='consumers-enable'),
    re_path(r'^(?P<consumer_id>[0-9a-zA-Z\-_(){}%]+)/disable$',
        DisableView.as_view(),
        name='consumers-disable'),
    re_path(r'^(?P<consumer_id>[0-9a-zA-Z\-_(){}%]+)/usage-data$',
        UsageDataAjaxView.as_view(),
        name='consumers-usage-data'),
]
