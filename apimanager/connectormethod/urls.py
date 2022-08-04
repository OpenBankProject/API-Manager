# -*- coding: utf-8 -*-
"""
URLs for config app
"""

from django.conf.urls import url

from connectormethod.views import IndexView, connectormethod_save, DetailView

urlpatterns = [
    url(r'^$',
        IndexView.as_view(),
        name='connectormethod'),
    url(r'save/connectormethod', connectormethod_save,
        name='connectormethod-save'),
    url(r'^my-connectormethod-ids/(?P<connectormethod_id>[\w\@\.\+-]+)$',
            DetailView.as_view(),
           name='connector_detail'),
]
"""url(r'^my-connectormethod-ids/(?P<connectormethod-id>[\w\@\.\+-]+)$',
        DetailView.as_view(),
       name='my-api-collection-detail'),
    url(r'^delete/api-collections/(?P<api_collection_id>[\w-]+)/api-collection-endpoint/(?P<operation_id>[\w\@\.\+-]+)$',
        DeleteCollectionEndpointView.as_view(),
        name='delete-api-collection-endpoint'),"""