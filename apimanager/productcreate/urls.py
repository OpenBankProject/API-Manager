# -*- coding: utf-8 -*-
"""
URLs for metrics app
"""

from django.conf.urls import url
from .views import IndexProductView, UpdateProductView

urlpatterns = [
    url(r'^create',
        IndexProductView.as_view(),
        name='products-create'),
    url(r'^update/(?P<bank_id>[ 0-9\w|\W\@\.\+-]+)/products/(?P<product_code>[0-9\w\@\.\+-]+)/attributes/(?P<product_attributes_id>[0-9\w\@\.\+-]+)$',
        UpdateProductView.as_view(),
        name='products_update'),
]
