# -*- coding: utf-8 -*-
"""
URLs for users app
"""

from django.conf.urls import url

from .views import IndexView, DetailView, MyDetailView, DeleteEntitlementView,InvitationView

urlpatterns = [
    url(r'^all$',
        IndexView.as_view(),
        name='users-index'),
    url(r'^all/user_id/(?P<user_id>[\w\@\.\+-]+)$',
        DetailView.as_view(),
        name='users-detail'),
    url(r'^myuser/user_id/(?P<user_id>[\w\@\.\+-]+)$',
        MyDetailView.as_view(),
        name='my-user-detail'),
    url(r'^myuser/invitation$',
        InvitationView.as_view(),
        name='my-user-invitation'),
    url(r'^(?P<user_id>[\w-]+)/entitlement/delete/(?P<entitlement_id>[\w-]+)$',
        DeleteEntitlementView.as_view(),
        name='users-delete-entitlement'),
]
