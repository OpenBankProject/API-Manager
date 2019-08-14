# -*- coding: utf-8 -*-
"""
URLs for config app
"""

from django.conf.urls import url

from .views import IndexView, methodrouting_save

urlpatterns = [
    url(r'^$',
        IndexView.as_view(),
        name='methodrouting-index'),
    url(r'save/method', methodrouting_save,
        name='methodrouting-save'),
]
