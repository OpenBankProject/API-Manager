# -*- coding: utf-8 -*-
"""
URLs for users app
"""

from django.conf.urls import url

from .views import IndexView, DetailView, AddEntitlementView, DeleteEntitlementView

urlpatterns = [
    url(r'^$',
        IndexView.as_view(),
        name='users-index'),
    url(r'^(?P<user_email>[\w\@\.\+-]+)$',
        DetailView.as_view(),
        name='users-detail'),
    url(r'^(?P<user_id>[\w-]+)/entitlement/add$',
        AddEntitlementView.as_view(),
        name='users-add-entitlement'),
    url(r'^(?P<user_id>[\w-]+)/entitlement/delete/(?P<entitlement_id>[\w-]+)$',
        DeleteEntitlementView.as_view(),
        name='users-delete-entitlement'),
]
