# -*- coding: utf-8 -*-
"""
URLs for metrics app
"""

from django.conf.urls import url
from .views import IndexAccountsView
#UpdateAccountsView

urlpatterns = [
    url(r'^create',
        IndexAccountsView.as_view(),
        name='accounts-create'),

]
"""url(r'^update/(?P<account_id>[ 0-9\w|\W\@\.\+-]+)/bank/(?P<bank_id>[0-9\w\@\.\+-]+)/$',
           UpdateAccountsView.as_view(),
           name='accounts_update'),"""