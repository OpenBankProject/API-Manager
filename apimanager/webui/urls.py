# -*- coding: utf-8 -*-
"""
URLs for config app
"""

from django.conf.urls import url

from .views import IndexView, webui_save

urlpatterns = [
    url(r'^$',
        IndexView.as_view(),
        name='webui-index'),
    url(r'save/method', webui_save,
        name='methodrouting-save'),
]
