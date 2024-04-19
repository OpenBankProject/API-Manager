# -*- coding: utf-8 -*-
"""
URLs for users app
"""

from django.conf.urls import url
from django.urls import path

from .views import IndexView, DetailView, MyDetailView, DeleteEntitlementView, InvitationView, UserStatusUpdateView, \
    ExportCsvView, AutocompleteFieldView, DeleteAttributeView

urlpatterns = [
    url(r'^all$',
        IndexView.as_view(),
        name='users-index'),
    url(r'^all/user_id/(?P<user_id>[\w\@\.\+-]+)$',
        DetailView.as_view(),
        name='users-detail'),
    url(r'^myuser$',
        MyDetailView.as_view(),
        name='my-user-detail'),
    url(r'^myuser/invitation$',
        InvitationView.as_view(),
        name='my-user-invitation'),
    url(r'^(?P<user_id>[\w-]+)/entitlement/delete/(?P<entitlement_id>[\w-]+)$',
        DeleteEntitlementView.as_view(),
        name='users-delete-entitlement'),
    url(r'^(?P<user_id>[\w-]+)/atribute/delete/(?P<user_attribute_id>[\w-]+)$',
        DeleteAttributeView.as_view(),
        name='users-delete-attribute'),
    url(r'^(?P<user_id>[\w-]+)/userStatusUpdateView/(?P<username>[\w\@\.\+-]+)$',
        UserStatusUpdateView.as_view(),
        name='user-status-update'),
    url(r'^export_csv$',
        ExportCsvView.as_view(),
        name='export-csv-users'),
]
