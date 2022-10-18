# -*- coding: utf-8 -*-
"""
URLs for System View app
"""

from django.conf.urls import url
from .views import SystemView

urlpatterns = [
    url(r'^$',
        SystemView.as_view(),
        name='system_view'),
]
