# -*- coding: utf-8 -*-
"""
URLs for metrics app
"""

from django.conf.urls import url

from .views import IndexProductView, UpdateProductView, createList

urlpatterns = [
    url(r'^create',
        IndexProductView.as_view(),
        name='products-create'),
    url(r'^update/(?P<product_code>[0-9\w\@\.\+-]+)/bank/(?P<bank_id>[0-9\w\@\.\+-]+)/$',
               UpdateProductView.as_view(),
               name='products_update'),
    url(r'^createProductList',
       createList,
       name = 'create-product-list'),
]
