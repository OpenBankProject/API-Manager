# -*- coding: utf-8 -*-
"""
URLs for config app
"""

from django.conf.urls import url

from apicollections.views import IndexView, apicollections_save, apicollections_delete, DetailView, DeleteCollectionEndpointView

urlpatterns = [
    url(r'^$',
        IndexView.as_view(),
        name='apicollections-index'),
    url(r'save/apicollection', apicollections_save,
        name='apicollection-save'),
    url(r'delete/apicollection', apicollections_delete,
        name='apicollection-delete'),
    url(r'^my-api-collection-ids/(?P<api_collection_id>[\w\@\.\+-]+)$',
        DetailView.as_view(),
        name='my-api-collection-detail'),
    url(r'^delete/api-collections/(?P<api_collection_id>[\w-]+)/api-collection-endpoint/(?P<operation_id>[\w\@\.\+-]+)$',
        DeleteCollectionEndpointView.as_view(),
        name='delete-api-collection-endpoint'),
    # url(r'^add/api-collections/(?P<api_collection_id>[\w-]+)/api-collection-endpoints/(?P<operation_id>[\w\@\.\+-]+)$',
    #     AddCollectionEndpointView.as_view(),
    #     name='add-api-collection-endpoint'),
]
