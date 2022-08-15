# -*- coding: utf-8 -*-
"""
Views of config app
"""

import json
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, HttpResponse
from django.views.generic import FormView
from obp.api import API, APIError
from django.urls import reverse, reverse_lazy
from base.utils import exception_handle, error_once_only
from .forms import ConnectorMethodForm
from django.views.decorators.csrf import csrf_exempt


class IndexView(LoginRequiredMixin, FormView):
    """Index view for config"""
    template_name = r"connectormethod/index.html"
    form_class = ConnectorMethodForm
    success_url = reverse_lazy('connectormethod-index')

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        api = API(self.request.session.get('obp'))
        urlpath = '/management/connector-methods'
        connectormethod =[]
        try:
            response = api.get(urlpath)
            if 'code' in response and response['code'] >= 400:
                error_once_only(self.request, response['message'])
            else:
                connectormethod=response['connector_methods']
        except APIError as err:
            error_once_only(self.request, Exception("OBP-API server is not running or do not response properly. "
                                                   "Please check OBP-API server.    "
                                                   "Details: " + str(err)))
        except BaseException as err:
            error_once_only(self.request, (Exception("Unknown Error. Details:" + str(err))))
        else:
            # set the default endpoint there, the first item will be the new endpoint.
            default_api_endpoint = {
                "api_collection_name": "Customer",
                "is_sharable": "True",
                "description":"Describe the purpose of the collection"
            }
            connectormethod.insert(0,json.dumps(default_api_endpoint))

            context.update({
                'connectormethods': connectormethod
            })
        return context

@exception_handle
@csrf_exempt
def connectormethod_save(request):
    api = API(request.session.get('obp'))
    urlpath = '/management/connector-methods'
    payload = {
        'method_name': request.POST.get('connector_method_name').strip(),
        'programming_lang': request.POST.get('connector_method_programming_lang'),
        'method_body': request.POST.get('connector_method_body').strip()
    }
    result = api.post(urlpath, payload = payload)
    return result


@exception_handle
@csrf_exempt
def connectormethod_update(request):
    connector_method_id = request.POST.get('connector_method_id').strip()
    urlpath = '/management/connector-methods/{}'.format(connector_method_id)
    api = API(request.session.get('obp'))
    payload = {
        'programming_lang': request.POST.get('connector_method_programming_lang_update'),
        'method_body': request.POST.get('connector_method_body_update').strip()
    }
    result = HttpResponse(content_type = 'application/json')
    result = api.put(urlpath, payload=payload)
    return result
