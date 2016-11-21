# -*- coding: utf-8 -*-
"""
URLs for OAuth 1 app
"""

from django.conf.urls import url

from .views import InitiateView, AuthorizeView, LogoutView

urlpatterns = [
    url(r'^initiate$', InitiateView.as_view(), name='oauth-initiate'),
    url(r'^authorize$', AuthorizeView.as_view(), name='oauth-authorize'),
    url(r'^logout$', LogoutView.as_view(), name='oauth-logout'),
]
