# -*- coding: utf-8 -*-
"""
URLs for metrics app
"""

from django.conf.urls import url

from .views import IndexBranchesView, UpdateBranchesView

urlpatterns = [
    url(r'^$',
        IndexBranchesView.as_view(),
        name='branches_list'),
    url(r'^update/(?P<branch_id>[0-9\w\@\.\+-]+)/bank/(?P<bank_id>[0-9\w\@\.\+-]+)/$',
        UpdateBranchesView.as_view(),
        name='branches_update')
]
