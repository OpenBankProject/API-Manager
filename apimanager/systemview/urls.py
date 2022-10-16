# -*- coding: utf-8 -*-
"""
URLs for System View app
"""

from django.conf.urls import url
from .views import SystemView # ExportCsvView

urlpatterns = [
    url(r'^$',
        SystemView.as_view(),
        name='system_view'),

]
"""url(r'^export_csv$',
           ExportCsvView.as_view(),
           name='export-csv')"""