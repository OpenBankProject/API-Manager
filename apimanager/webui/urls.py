# -*- coding: utf-8 -*-
"""
URLs for config app
"""

from django.conf.urls import url

from .views import IndexView, webui_save, webui_delete

urlpatterns = [
    url(r'^$',
        IndexView.as_view(),
        name='webui-index'),
    url(r'save/method', webui_save,
        name='methodrouting-save'),
    url(r'delete/method', webui_delete,
        name='methodrouting-delete')
]
