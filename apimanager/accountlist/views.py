from django.shortcuts import render

# Create your views here.
# -*- coding: utf-8 -*-
"""
Views of Account List app
"""
import datetime
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
import json
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.views.generic import FormView,TemplateView, View
from accounts.views import IndexAccountsView
from obp.api import API, APIError
from base.views import get_banks
import csv

class AccountListView(IndexAccountsView, LoginRequiredMixin, FormView ):
    template_name = "accountlist/accountlist.html"
    success_url = '/accounts/list'

    def get_accountlist(self, context):
        api = API(self.request.session.get('obp'))
        try:
            #self.bankids = self.get_banks()
            accounts_list = []
            #for bank_id in self.bankids:
            urlpath = '/my/accounts'
            result = api.get(urlpath)
            if 'accounts' in result:
                accounts_list.extend(result['accounts'])
        except APIError as err:
            messages.error(self.request, err)
            return []
        except Exception as inst:
            messages.error(self.request, "Unknown Error {}".format(type(inst).__name__))
            return []
        return accounts_list
    def get_context_data(self, **kwargs):
            context = super(IndexAccountsView, self).get_context_data(**kwargs)
            accounts_list = self.get_accountlist(context)
            context.update({
                'accounts_list': accounts_list,
                #'bankids': bankids
            })
            return context
class ExportCsvView(LoginRequiredMixin, View):
    """View to export the user to csv"""

    def get(self, request, *args, **kwargs):
       api = API(self.request.session.get('obp'))
       try:
           self.bankids = get_banks(self.request)
           accounts_list = []
           for bank_id in self.bankids:
               urlpath = '/banks/{}/accounts'.format(bank_id)
               result = api.get(urlpath)
               if 'accounts' in result:
                   accounts_list.extend(result['accounts'])
       except APIError as err:
           messages.error(self.request, err)
       except Exception as inst:
           messages.error(self.request, "Unknown Error {}".format(type(inst).__name__))
       response = HttpResponse(content_type = 'text/csv')
       response['Content-Disposition'] = 'attachment;filename= Account'+ str(datetime.datetime.now())+'.csv'
       writer = csv.writer(response)
       writer.writerow(["id","label","bank_id","account_type","scheme","address","id", "short_name", "description", "is_public"])
       for user in accounts_list:
          writer.writerow([user['id'],user['label'], user['bank_id'], user["account_type"], user["scheme"], user["address"], user["views"]['id'],
                             user["views"]['short_name'], user["views"]['description'], user["views"]['is_public']])
       return response


