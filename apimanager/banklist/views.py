from django.shortcuts import render

# Create your views here.
# -*- coding: utf-8 -*-
"""
Views of Bank List app
"""
import datetime
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
import json
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.views.generic import FormView,TemplateView, View
from banks.views import IndexBanksView
from obp.api import API, APIError


class BankListView(IndexBanksView, LoginRequiredMixin, FormView ):
    template_name = "banklist/banklist.html"
    success_url = '/banks/list'

    def get_banks(self,context):
        api = API(self.request.session.get('obp'))
        try:
            urlpath = 'v5.1.0/banks'
            result = api.get(urlpath)
            banks_list = []
            if 'banks' in result:
                banks_list.extend(result["banks"])
        except APIError as err:
            messages.error(self.request, err)
            return []
        except Exception as inst:
            messages.error(self.request, "Unknown Error {}".format(type(inst).__name__))
            return []

        return banks_list
    def get_context_data(self, **kwargs):
        context = super(BankListView, self).get_context_data(**kwargs)
        banks_list = self.get_banks(context)
        context.update({
            'banks_list': banks_list
        })
        return context
