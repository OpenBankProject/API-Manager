# -*- coding: utf-8 -*-
"""
URLs for Product list app
"""

from django.conf.urls import url
from .views import ProductListView, ExportCsvView

urlpatterns = [
    url(r'^$',
        ProductListView.as_view(),
        name='product-list'),
    url(r'^export_csv$',
            ExportCsvView.as_view(),
            name='export-csv')
]
