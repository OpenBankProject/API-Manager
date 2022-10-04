# -*- coding: utf-8 -*-
"""
URLs for ATM list app
"""

from django.conf.urls import url
from .views import AtmListView, ExportCsvView

urlpatterns = [
    url(r'^$',
        AtmListView.as_view(),
        name='atm-list'),
    url(r'^export_csv$',
            ExportCsvView.as_view(),
            name='export-csv')
]
