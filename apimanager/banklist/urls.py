# -*- coding: utf-8 -*-
"""
URLs for Bank list app
"""

from django.conf.urls import url
from .views import BankListView #, ExportCsvView

urlpatterns = [
    url(r'^$',
        BankListView.as_view(),
        name='bank-list'),

]
"""
url(r'^export_csv$',
            ExportCsvView.as_view(),
            name='export-bank-csv') """
