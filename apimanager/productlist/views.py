from django.shortcuts import render

# Create your views here.
# -*- coding: utf-8 -*-
"""
Views of atms app
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

class ProductListView(LoginRequiredMixin, FormView ):
    template_name = "productlist/productlist.html"
    success_url = '/products/list'
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

    def get_products(self):
            api = API(self.request.session.get('obp'))
            try:
                self.bankids = self.get_banks()
                products_list = []
                for bank_id in self.bankids:
                    urlpath = '/banks/{}/products'.format(bank_id)
                    result = api.get(urlpath)
                    #print(result, "This is a result")
                    if 'products' in result:
                        products_list.extend(result['products'])
            except APIError as err:
                messages.error(self.request, err)
                return []
            except Exception as inst:
                messages.error(self.request, "Unknown Error {}".format(type(inst).__name__))
                return []
            return products_list
    def get_context_data(self, **kwargs):
            products_list = self.get_products()
            context = {}
            context.update({
                'products_list': products_list,
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
           products_list = []
           for bank_id in self.bankids:
               urlpath = '/banks/{}/products'.format(bank_id)
               result = api.get(urlpath)
               #print(result)
               if 'products' in result:
                   products_list.extend(result['products'])
       except APIError as err:
           messages.error(self.request, err)
       except Exception as inst:
           messages.error(self.request, "Unknown Error {}".format(type(inst).__name__))
       response = HttpResponse(content_type = 'text/csv')
       response['Content-Disposition'] = 'attachment;filename= Atms'+ str(datetime.datetime.now())+'.csv'
       writer = csv.writer(response)
       writer.writerow(["product_code","bank_id","name","parent_product_code","more_info_url","terms_and_conditions_url","description", "license", "id", "name"])
       for user in atms_list:
          writer.writerow([user['product_code'],user['bank_id'], user['name'], user["parent_product_code"], user["more_info_url"],
                             user["terms_and_conditions_url"], user["description"], user["license"]['id'], user["license"]['name']])
       return response

       #print(atms_list)

