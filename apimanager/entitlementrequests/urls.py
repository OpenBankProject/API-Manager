# -*- coding: utf-8 -*-
"""
URLs for entitlement requests app
"""

from django.conf.urls import url

from .views import IndexView

urlpatterns = [
    url(r'^$',
        IndexView.as_view(),
        name='entitlementrequests-index'),
]
