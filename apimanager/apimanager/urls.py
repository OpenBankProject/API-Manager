# -*- coding: utf-8 -*-
"""
URLs for apimanager
"""

from django.conf.urls import url, include

from base.views import HomeView


urlpatterns = [
    url(r'^$', HomeView.as_view(), name="home"),
    url(r'^oauth/', include('oauth.urls')),
    url(r'^consumers/', include('consumers.urls')),
    url(r'^users/', include('users.urls')),
    url(r'^customers/', include('customers.urls')),
    url(r'^metrics/', include('metrics.urls')),
    url(r'^config/', include('config.urls')),
]
