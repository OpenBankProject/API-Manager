# -*- coding: utf-8 -*-
"""
URLs for Account list app
"""

from django.conf.urls import url
from .views import AccountListView, ExportCsvView

urlpatterns = [
    url(r'^$',
        AccountListView.as_view(),
        name='account-list'),
    url(r'^export_csv$',
        ExportCsvView.as_view(),
        name='export-csv-account')
]
