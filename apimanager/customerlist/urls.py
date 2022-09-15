# -*- coding: utf-8 -*-
"""
URLs for metrics app
"""

from django.conf.urls import url
from .views import CustomerListView, ExportCsvView

urlpatterns = [
    url(r'^$',
        CustomerListView.as_view(),
        name='customer-list-views'),
    url(r'^export_csv$',
            ExportCsvView.as_view(),
            name='export-csv')
]
