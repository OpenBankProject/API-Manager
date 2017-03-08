# -*- coding: utf-8 -*-
"""
URLs for metrics app
"""

from django.conf.urls import url

from .views import IndexView

urlpatterns = [
    url(r'^$',
        IndexView.as_view(),
        name='metrics-index'),
]
