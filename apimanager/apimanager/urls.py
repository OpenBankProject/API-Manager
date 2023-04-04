# -*- coding: utf-8 -*-
"""
URLs for apimanager
"""

from django.conf.urls import url, include
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
    url(r'^oauth/initiate$',
        OAuthInitiateView.as_view(), name='oauth-initiate'),
    url(r'^oauth/authorize$',
            OAuthAuthorizeView.as_view(), name='oauth-authorize'),
    url(r'^directlogin$',
            DirectLoginView.as_view(), name='directlogin'),
    url(r'^gatewaylogin$',
            GatewayLoginView.as_view(), name='gatewaylogin'),
    # Defining authentication URLs here and not including oauth.urls for
    # backward compatibility
]
urlpatterns += i18n_patterns(
#urlpatterns = (
    url(r'^$', HomeView.as_view(), name="home"),
    url(r'^single-sign-on',
        OAuthInitiateView.as_view(), name='single-sign-on'),
    url(r'^logout$', LogoutView.as_view(), name='oauth-logout'),
    url(r'^systemviews/', include('systemviews.urls')),
    url(r'^accounts/', include('accounts.urls')),
    url(r'^account/list', include('accountlist.urls')),
    url(r'^consumers/', include('consumers.urls')),
    url(r'^entitlementrequests/', include('entitlementrequests.urls')),
    url(r'^users/', include('users.urls')),
    url(r'^branches/', include('branches.urls')),
    url(r'^atms/', include('atms.urls')),
    url(r'^atms/list', include('atmlist.urls')),
    url(r'^banks/', include('banks.urls')),
    url(r'^banks/list', include('banklist.urls')),
    url(r'^products/', include('products.urls')),
    url(r'^products/list', include('productlist.urls')),
    url(r'^customers/', include('customers.urls')),
    url(r'^customer/list', include('customerlist.urls')),
    url(r'^metrics/', include('metrics.urls')),
    url(r'^config/', include('config.urls')),
    url(r'^webui/', include('webui.urls')),
    url(r'^methodrouting/', include('methodrouting.urls')),
    url(r'^connectormethod/', include('connectormethod.urls')),
    url(r'^dynamicendpoints/', include('dynamicendpoints.urls')),
    url(r'^apicollections/', include('apicollections.urls')),
    url(r'^apicollections-list', include('apicollectionlist.urls')),
)
    #prefix_default_language=False,
#)+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)