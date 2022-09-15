from django.shortcuts import render

# Create your views here.
# -*- coding: utf-8 -*-
"""
Views of Customer List app
"""
import datetime
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
import json
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.views.generic import FormView,TemplateView, View
from customers.views import CreateView
from obp.api import API, APIError
import csv



class CustomerListView(CreateView, LoginRequiredMixin, FormView ):
    template_name = "customersView/customerlist.html"
    success_url = '/customersView/'
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

    def get_context_data(self, **kwargs):
            context = super(CreateView, self).get_context_data(**kwargs)
            customer_list = self.get_atms(context)
            context.update({
                'customers_list': customers_list,
                'bankids': self.bankids
            })
            return context
class ExportCsvView(LoginRequiredMixin, View):
    """View to export the user to csv"""
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
    def get(self, request, *args, **kwargs):
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
       except Exception as inst:
           messages.error(self.request, "Unknown Error {}".format(type(inst).__name__))
       response = HttpResponse(content_type = 'text/csv')
       response['Content-Disposition'] = 'attachment;filename= Atms'+ str(datetime.datetime.now())+'.csv'
       writer = csv.writer(response)
       writer.writerow(["id","name","notes","line_1","line_2","line_3","city", "county", "state", "postcode","country_code", "longitude","latitude","more_info"])
       for user in atms_list:
          writer.writerow([user['id'],user['name'], user['notes'], user["address"]['line_1'], user["address"]['line_2'],
                             user["address"]['line_3'], user["address"]['city'], user["address"]['county'], user["address"]['state'], user["address"]['postcode'], user["address"]['country_code'], user["location"]['longitude'], user["location"]['latitude'], user['more_info']])
       return response

       #print(atms_list)

