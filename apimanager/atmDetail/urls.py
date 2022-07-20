# -*- coding: utf-8 -*-
"""
URLs for metrics app
"""

from django.conf.urls import url
from .views import AtmListView

urlpatterns = [
    url(r'^$',
        AtmListView.as_view(),
        name='atm_detail')
]
