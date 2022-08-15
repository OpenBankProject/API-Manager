# -*- coding: utf-8 -*-
"""
URLs for config app
"""

from django.conf.urls import url

from connectormethod.views import IndexView, connectormethod_save, connectormethod_update

urlpatterns = [
    url(r'^$',
        IndexView.as_view(),
        name='connectormethod'),
    url(r'save/connectormethod', connectormethod_save,
        name='connectormethod-save'),
    url(r'^update/connectormethod', connectormethod_update,
        name='connectormethod-update')
]
