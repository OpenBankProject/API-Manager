# -*- coding: utf-8 -*-
"""
URLs for Bank app
"""

from django.conf.urls import url
from banks.views import IndexBanksView, UpdateBanksView, bank_attribute_save, bank_attribute_update, bank_attribute_delete

urlpatterns = [
    url(r'^create',
        IndexBanksView.as_view(),
        name='banks_create'),
    url(r'^update/bank/(?P<bank_id>[0-9\w\@\.\+-]+)/$',
        UpdateBanksView.as_view(),
        name='banks_update'),
    url(r'save/attribute', bank_attribute_save,
        name='bank_attribute_save'),
    url(r'updateattribute/attribute', bank_attribute_update,
        name='bank_attribute_update'),
    url(r'delete/attribute', bank_attribute_delete,
        name='bank_attribute_delete'),
]