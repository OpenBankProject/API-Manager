# -*- coding: utf-8 -*-
"""
URLs for Account app
"""

from django.conf.urls import url
from .views import IndexAccountsView

urlpatterns = [
    url(r'^create',
        IndexAccountsView.as_view(),
        name='accounts-create'),

]
