# -*- coding: utf-8 -*-
"""
URLs for customers app
"""

from django.conf.urls import url
from .views import CreateView

urlpatterns = [
    url(r'^$',
        CreateView.as_view(),
        name='customers-create'),
]
