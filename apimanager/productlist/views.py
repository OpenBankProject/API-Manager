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
from products.views import IndexProductView
from obp.api import API, APIError
from base.views import get_banks
import csv

#import csv

class ProductListView(IndexProductView, LoginRequiredMixin, FormView ):
    template_name = "productlist/productlist.html"
    success_url = '/products/list'

    def get_products(self, context):
        api = API(self.request.session.get('obp'))
        try:
            self.bankids = get_banks(self.request)
            products_list = []
            for bank_id in self.bankids:
                urlpath = '/banks/{}/products'.format(bank_id)
                result = api.get(urlpath)
                if 'products' in result:
                    products_list.extend(result['products'])
        except APIError as err:
            messages.error(self.request, err)
            return []
        except Exception as inst:
            messages.error(self.request, "Unknown Error {}".format(type(inst).__name__))
            return []
        print(products_list, "This is a product list")
        return products_list

    def get_context_data(self, **kwargs):
        context = super(IndexProductView, self).get_context_data(**kwargs)
        products_list = self.get_products(context)
        context.update({
            'products_list': products_list,
            'bankids': self.bankids
        })
        return context
class ExportCsvView(LoginRequiredMixin, View):
    """View to export the user to csv"""

    def get(self, request, *args, **kwargs):
       api = API(self.request.session.get('obp'))
       products_list = []
       try:
           self.bankids = get_banks(self.request)
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
       response['Content-Disposition'] = 'attachment;filename= Product'+ str(datetime.datetime.now())+'.csv'
       writer = csv.writer(response)
       writer.writerow(["product_code","bank_id","name","parent_product_code","more_info_url","terms_and_conditions_url","description"])
       for user in products_list:
          writer.writerow([user['product_code'],user['bank_id'], user['name'], user["parent_product_code"], user["more_info_url"],
                             user["terms_and_conditions_url"], user["description"]])
       return response

       #print(atms_list)
