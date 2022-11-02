from django.shortcuts import render

# Create your views here.
# -*- coding: utf-8 -*-
"""
Views of Api Collection list app
"""
import datetime
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
import json
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.views.generic import FormView,TemplateView, View
from apicollections.views import IndexView
from obp.api import API, APIError
import csv



class ApiCollectionListView(IndexView, LoginRequiredMixin, FormView ):
    template_name = "apicollectionlist/apicollectionlist.html"
    success_url = '/apicollections/list'

    def get_apicollections(self, context):
        api = API(self.request.session.get('obp'))
        try:
            apicollections_list = []
            urlpath = '/my/api-collections'
            result = api.get(urlpath)
            if 'api_collections' in result:
                apicollections_list.extend(result['api_collections'])
        except APIError as err:
            messages.error(self.request, err)
            return []
        except Exception as inst:
            messages.error(self.request, "Unknown Error {}".format(type(inst).__name__))
            return []

        return apicollections_list

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        apicollections_list = self.get_apicollections(context)
        context.update({
            'apicollections_list': apicollections_list,
        })
        return context

class ExportCsvView(LoginRequiredMixin, View):
    """View to export the user to csv"""

    def get(self, request, *args, **kwargs):
       api = API(self.request.session.get('obp'))
       try:
           apicollections_list = []
           urlpath = '/my/api-collections'
           result = api.get(urlpath)
           if 'api_collections' in result:
               apicollections_list.extend(result['api_collections'])
       except APIError as err:
           messages.error(self.request, err)
       except Exception as inst:
           messages.error(self.request, "Unknown Error {}".format(type(inst).__name__))
       response = HttpResponse(content_type = 'text/csv')
       response['Content-Disposition'] = 'attachment;filename= ApiCollections'+ str(datetime.datetime.now())+'.csv'
       writer = csv.writer(response)
       writer.writerow(["api_collection_id","user_id","api_collection_name","is_sharable","description"])
       for user in apicollections_list:
          writer.writerow([user['api_collection_id'],user['user_id'], user['api_collection_name'], user["is_sharable"],
                             user["description"]])
       return response


