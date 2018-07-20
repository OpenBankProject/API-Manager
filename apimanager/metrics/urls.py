# -*- coding: utf-8 -*-
"""
URLs for metrics app
"""

from django.conf.urls import url

from .views import (
    APIMetricsView,
    APISummaryPartialFunctionView,
    ConnectorMetricsView,
    MetricsSummaryView,
    YearlySummaryView,
    QuarterlySummaryView,
    WeeklySummaryView,
    DailySummaryView,
    HourlySummaryView,
    CustomSummaryView
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
    url(r'^summary/$',
        MetricsSummaryView.as_view(),
        name='metrics-summary'),
    url(r'^yearly-summary/$',
        YearlySummaryView.as_view(),
        name='yearly-summary'),
    url(r'^quarterly-summary/$',
        QuarterlySummaryView.as_view(),
        name='quarterly-summary'),
    url(r'^weekly-summary/$',
        WeeklySummaryView.as_view(),
        name='weekly-summary'),
    url(r'^daily-summary/$',
        DailySummaryView.as_view(),
        name='daily-summary'),
    url(r'^hourly-summary/$',
        HourlySummaryView.as_view(),
        name='hourly-summary'),
    url(r'^custom-summary/$',
        CustomSummaryView.as_view(),
        name='custom-summary'),
]
