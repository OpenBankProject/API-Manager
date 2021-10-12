# -*- coding: utf-8 -*-
"""
URLs for config app
"""

from django.conf.urls import url

from apicollections.views import IndexView, apicollections_save, apicollections_delete

urlpatterns = [
    url(r'^$',
        IndexView.as_view(),
        name='apicollections-index'),
    url(r'save/apicollection', apicollections_save,
        name='apicollection-save'),
    url(r'delete/apicollection', apicollections_delete,
        name='apicollection-delete')
]
