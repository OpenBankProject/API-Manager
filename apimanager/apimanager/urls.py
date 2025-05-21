# -*- coding: utf-8 -*-
"""
URLs for apimanager
"""

from django.urls import re_path, include
from django.conf.urls.i18n import i18n_patterns

from base.views import HomeView
from obp.views import (
    OAuthInitiateView, OAuthAuthorizeView,
    DirectLoginView,
    GatewayLoginView,
    LogoutView,
)

urlpatterns = [
    #These pages URLs have no GUI
    re_path(r'^oauth/initiate$',
        OAuthInitiateView.as_view(), name='oauth-initiate'),
    re_path(r'^oauth/authorize$',
            OAuthAuthorizeView.as_view(), name='oauth-authorize'),
    re_path(r'^directlogin$',
            DirectLoginView.as_view(), name='directlogin'),
    re_path(r'^gatewaylogin$',
            GatewayLoginView.as_view(), name='gatewaylogin'),
    # Defining authentication URLs here and not including oauth.urls for
    # backward compatibility
]
urlpatterns += i18n_patterns(
#urlpatterns = (
    re_path(r'^$', HomeView.as_view(), name="home"),
    re_path(r'^single-sign-on',
        OAuthInitiateView.as_view(), name='single-sign-on'),
    re_path(r'^logout$', LogoutView.as_view(), name='oauth-logout'),
    re_path(r'^systemviews/', include('systemviews.urls')),
    re_path(r'^accounts/', include('accounts.urls')),
    re_path(r'^account/list', include('accountlist.urls')),
    re_path(r'^consumers/', include('consumers.urls')),
    re_path(r'^entitlementrequests/', include('entitlementrequests.urls')),
    re_path(r'^consents', include('consents.urls')),
    re_path(r'^users/', include('users.urls')),
    re_path(r'^branches/', include('branches.urls')),
    re_path(r'^atms/', include('atms.urls')),
    re_path(r'^atms/list', include('atmlist.urls')),
    re_path(r'^banks/', include('banks.urls')),
    re_path(r'^banks/list', include('banklist.urls')),
    re_path(r'^products/', include('products.urls')),
    re_path(r'^products/list', include('productlist.urls')),
    re_path(r'^customers/', include('customers.urls')),
    re_path(r'^customer/list', include('customerlist.urls')),
    re_path(r'^metrics/', include('metrics.urls')),
    re_path(r'^config/', include('config.urls')),
    re_path(r'^webui/', include('webui.urls')),
    re_path(r'^methodrouting/', include('methodrouting.urls')),
    re_path(r'^connectormethod/', include('connectormethod.urls')),
    re_path(r'^dynamicendpoints/', include('dynamicendpoints.urls')),
    re_path(r'^apicollections/', include('apicollections.urls')),
    re_path(r'^apicollections-list', include('apicollectionlist.urls')),
)
    #prefix_default_language=False,
#)+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)