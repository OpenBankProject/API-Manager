# -*- coding: utf-8 -*-
"""
URLs for metrics app
"""

from django.conf.urls import url
from .views import AtmListView, ExportCsvView

urlpatterns = [
    url(r'^$',
        AtmListView.as_view(),
        name='atm-detail'),
    url(r'^export_csv$',
            ExportCsvView.as_view(),
            name='export-csv')
]
