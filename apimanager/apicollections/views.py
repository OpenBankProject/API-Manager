# -*- coding: utf-8 -*-
"""
Views of config app
"""

import json
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import FormView
from obp.api import API, APIError
from base.utils import exception_handle, error_once_only
from .forms import ApiCollectionsForm
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt


class IndexView(LoginRequiredMixin, FormView):
    """Index view for config"""
    template_name = "apicollections/index.html"
    form_class = ApiCollectionsForm
    success_url = reverse_lazy('apicollections-index')

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        api = API(self.request.session.get('obp'))
        urlpath = '/my/api-collections'
        api_collections =[]
        try:
            response = api.get(urlpath)
            if 'code' in response and response['code'] >= 400:
                error_once_only(self.request, response['message'])
            else:
                api_collections=response['api_collections']
        except APIError as err:
            error_once_only(self.request, Exception("OBP-API server is not running or do not response properly. "
                                                   "Please check OBP-API server.    "
                                                   "Details: " + str(err)))
        except BaseException as err:
            error_once_only(self.request, (Exception("Unknown Error. Details:" + str(err))))
        else:
            # set the default endpoint there, the first item will be the new endpoint.
            default_api_endpoint = {
                "api_collection_name": "Testing",
                "is_sharable": True,
                "description":"This is for testing"
            }
            api_collections.insert(0,json.dumps(default_api_endpoint))
            
            context.update({
                'api_collections': api_collections
            })
        return context

@exception_handle
@csrf_exempt
def apicollections_save(request):
    api_collection_body = request.POST.get('api-collection-body')
    api = API(request.session.get('obp'))
    urlpath = '/my/api-collections'
    result = api.post(urlpath, payload =json.loads( api_collection_body))
    return result


@exception_handle
@csrf_exempt
def apicollections_delete(request):
    api_collection_id = request.POST.get('api_collection_id')

    api = API(request.session.get('obp'))
    urlpath = '/my/api-collections/{}'.format(api_collection_id)
    result = api.delete(urlpath)
    return result
