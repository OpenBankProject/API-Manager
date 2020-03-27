# -*- coding: utf-8 -*-
"""
URLs for config app
"""

from django.conf.urls import url

from dynamicendpoints.views import IndexView, dynamicendpoints_save

urlpatterns = [
    url(r'^$',
        IndexView.as_view(),
        name='dynamicendpoints-index'),
    url(r'save/dynamicendpoint', dynamicendpoints_save,
        name='dynamicendpoint-save')
]
