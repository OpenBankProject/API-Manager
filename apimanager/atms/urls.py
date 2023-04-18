# -*- coding: utf-8 -*-
"""
URLs for metrics app
"""

from django.conf.urls import url
from atms.views import IndexAtmsView, UpdateAtmsView, atm_attribute_save, atm_attribute_delete, atm_attribute_update

urlpatterns = [
    url(r'^create',
        IndexAtmsView.as_view(),
        name='atms_create'),
    url(r'^update/(?P<atm_id>[ 0-9\w|\W\@\.\+-]+)/bank/(?P<bank_id>[0-9\w\@\.\+-]+)/$',
        UpdateAtmsView.as_view(),
        name='atms_update'),
    url(r'save/attribute', atm_attribute_save,
        name='atm_attribute_save'),
    url(r'delete/attribute', atm_attribute_delete,
        name='atm_attribute_delete'),
    url(r'updateattribute/attribute', atm_attribute_update,
        name='atm_attribute_update'),
]
