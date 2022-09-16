# -*- coding: utf-8 -*-
"""
URLs for metrics app
"""

from django.conf.urls import url
from .views import IndexAtmsView, UpdateAtmsView

urlpatterns = [
    url(r'^create',
        IndexAtmsView.as_view(),
        name='atms_create'),
    url(r'^update/(?P<atm_id>[ 0-9\w|\W\@\.\+-]+)/bank/(?P<bank_id>[0-9\w\@\.\+-]+)/$',
        UpdateAtmsView.as_view(),
        name='atms_update'),
]
