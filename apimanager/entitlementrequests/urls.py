# -*- coding: utf-8 -*-
"""
URLs for entitlement requests app
"""

from django.conf.urls import url

from .views import IndexView, RejectEntitlementRequest, AcceptEntitlementRequest

urlpatterns = [
    url(r'^$',
        IndexView.as_view(),
        name='entitlementrequests-index'),
    url(r'^entitlement-requests/entitlement_request_id/(?P<entitlement_request_id>[\w\@\.\+-]+)$',
        RejectEntitlementRequest.as_view(),
        name='entitlement-request-delete'),
    url(r'^entitlement-requests/user_id/(?P<user_id>[\w\@\.\+-]+)$',
        AcceptEntitlementRequest.as_view(),
        name='entitlement-request-accept'),
]
