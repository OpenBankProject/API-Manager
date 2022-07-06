from django.shortcuts import render

# Create your views here.
# -*- coding: utf-8 -*-
"""
Views of atms app
"""
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
import json
from django.urls import reverse_lazy
from django.views.generic import FormView
from atms.views import IndexAtmsView
from obp.api import API, APIError


class AtmListView(IndexAtmsView, LoginRequiredMixin, FormView ):
    template_name = "atmsView/atm_List.html"
    success_url = '/atmsView/'
    def get_banks(self):
                api = API(self.request.session.get('obp'))
                try:
                    urlpath = '/banks'
                    result = api.get(urlpath)
                    if 'banks' in result:
                        return [bank['id'] for bank in sorted(result['banks'], key=lambda d: d['id'])]
                    else:
                        return []
                except APIError as err:
                    messages.error(self.request, err)
                    return []

    def get_atms(self, context):
            api = API(self.request.session.get('obp'))
            try:
                self.bankids = self.get_banks()
                atms_list = []
                for bank_id in self.bankids:
                    urlpath = '/banks/{}/atms'.format(bank_id)
                    result = api.get(urlpath)
                    #print(result)
                    if 'atms' in result:
                        atms_list.extend(result['atms'])
            except APIError as err:
                messages.error(self.request, err)
                return []
            except Exception as inst:
                messages.error(self.request, "Unknown Error {}".format(type(inst).__name__))
                return []

            return atms_list
    def get_context_data(self, **kwargs):
            context = super(IndexAtmsView, self).get_context_data(**kwargs)
            atms_list = self.get_atms(context)
            context.update({
                'atms_list': atms_list,
                'bankids': self.bankids
            })
            return context
