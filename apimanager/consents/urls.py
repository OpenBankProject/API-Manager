# -*- coding: utf-8 -*-
"""
URLs for entitlement requests app
"""

from django.urls import re_path

from .views import IndexView, RevokeConsents

urlpatterns = [
    re_path(r'^$',
        IndexView.as_view(),
        name='consents-index'),
    re_path(r'^consents/consent_id/(?P<consent_id>[\w\@\.\+-]+)$',
            RevokeConsents.as_view(),
        name='consent-revoke'),
]
