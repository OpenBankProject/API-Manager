# -*- coding: utf-8 -*-
"""
URLs for metrics app
"""

from django.conf.urls import url

from .views import (
    APIMetricsView,
    APISummaryPartialFunctionView,
    ConnectorMetricsView
)

urlpatterns = [
    url(r'^api/$',
        APIMetricsView.as_view(),
        name='api-metrics'),
    url(r'^api/summary-partial-function$',
        APISummaryPartialFunctionView.as_view(),
        name='api-metrics-summary-partial-function'),
    url(r'^connector/$',
        ConnectorMetricsView.as_view(),
        name='connector-metrics'),
]
