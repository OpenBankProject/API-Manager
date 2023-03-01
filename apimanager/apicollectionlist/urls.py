# -*- coding: utf-8 -*-
"""
URLs for Api Collection list app
"""

from django.conf.urls import url
from .views import ApiCollectionListView, ExportCsvView

urlpatterns = [
    url(r'^$',
        ApiCollectionListView.as_view(),
        name='apicollection-list'),
    url(r'^export_csv$',
        ExportCsvView.as_view(),
        name='export-csv-apicollection')
]
