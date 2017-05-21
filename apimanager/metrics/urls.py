# -*- coding: utf-8 -*-
"""
URLs for metrics app
"""

from django.conf.urls import url

from .views import IndexView, SummaryPartialFunctionView

urlpatterns = [
    url(r'^$',
        IndexView.as_view(),
        name='metrics-index'),
    url(r'^summary-partial-function$',
        SummaryPartialFunctionView.as_view(),
        name='metrics-summary-partial-function'),

]
