# -*- coding: utf-8 -*-
"""
URLs for config app
"""

from django.conf.urls import url

#from .views import IndexView, methodrouting_save, methodrouting_delete
from methodrouting.views import IndexView, methodrouting_save, methodrouting_delete

urlpatterns = [
    url(r'^$',
        IndexView.as_view(),
        name='methodrouting-index'),
    url(r'save/method', methodrouting_save,
        name='methodrouting-save'),
    url(r'delete/method', methodrouting_delete,
        name='methodrouting-delete'),
]
