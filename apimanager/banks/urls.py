# -*- coding: utf-8 -*-
"""
URLs for Bank app
"""

from django.conf.urls import url
from .views import IndexBanksView, UpdateBanksView

urlpatterns = [
    url(r'^create',
        IndexBanksView.as_view(),
        name='banks_create'),
    url(r'^update/bank/(?P<bank_id>[0-9\w\@\.\+-]+)/$',
        UpdateBanksView.as_view(),
        name='banks_update')
]