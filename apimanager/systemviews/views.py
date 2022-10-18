from django.shortcuts import render

# Create your views here.
# -*- coding: utf-8 -*-
"""
Views of System View app
"""
import datetime
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
import json
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.views.generic import FormView,TemplateView, View
from obp.api import API, APIError

import csv

class SystemView(LoginRequiredMixin, FormView):
    template_name = "systemviews/index.html"
    success_url = '/systemview'

    def get_systemview(self):
        api = API(self.request.session.get('obp'))
        try:
            system_view = []
            urlpath = '/system-views/owner'
            result = api.get(urlpath)
            system_view = result
        except APIError as err:
            messages.error(self.request, err)
            return []
        except Exception as inst:
            messages.error(self.request, "Unknown Error {}".format(type(inst).__name__))
            return []
        return system_view
    def get_context_data(self, **kwargs):
        system_view = self.get_systemview()
        context = {}
        context.update({
            'system_view': system_view,
        })
        return context
