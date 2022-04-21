# -*- coding: utf-8 -*-
"""
URLs for metrics app
"""

from django.conf.urls import url

from .views import IndexAtmView, UpdateAtmView

urlpatterns = [
    url(r'^$',
        IndexAtmView.as_view(),
        name='atms_list'),
    url(r'^update/(?P<atm_id>[0-9\w\@\.\+-]+)/bank/(?P<bank_id>[0-9\w\@\.\+-]+)/$',
        UpdateAtmView.as_view(),
        name='atms_update')
]
