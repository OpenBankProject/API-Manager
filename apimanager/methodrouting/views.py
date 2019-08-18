# -*- coding: utf-8 -*-
"""
Views of config app
"""

import json

from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import FormView
from obp.api import API, APIError
from .forms import MethodRoutingForm
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt

def error_once_only(request, err):
    """
    Just add the error once
    :param request:
    :param err:
    :return:
    """
    storage = messages.get_messages(request)
    if str(err) not in [str(m.message) for m in storage]:
        messages.error(request, err)

class IndexView(LoginRequiredMixin, FormView):
    """Index view for config"""
    template_name = "methodrouting/index.html"
    form_class = MethodRoutingForm
    success_url = reverse_lazy('methodrouting-index')

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        api = API(self.request.session.get('obp'))
        urlpath = '/management/method_routings?active=true'

        try:
            response = api.get(urlpath)
        except APIError as err:
            messages.error(self.request, Exception("OBP-API server is not running or do not response properly. "
                                                   "Please check OBP-API server.    "
                                                   "Details: " + str(err)))
        except BaseException as err:
            messages.error(self.request, (Exception("Unknown Error. Details:" + str(err))))
        else:
            context.update(response)
        return context

@csrf_exempt
def methodrouting_save(request):
    method_name = request.POST.get('method_name')
    connector_name = request.POST.get('connector_name')
    bank_id_pattern = request.POST.get('bank_id_pattern')
    is_bank_id_exact_match = request.POST.get('is_bank_id_exact_match')
    parameters = request.POST.get('parameters')
    method_routing_id = request.POST.get('method_routing_id')

    payload = {
        'method_name' : method_name,
        'connector_name': connector_name,
        'is_bank_id_exact_match': bool(is_bank_id_exact_match),
        'bank_id_pattern':bank_id_pattern,
        'parameters':eval(parameters),
        'method_routing_id':method_routing_id
    }

    api = API(request.session.get('obp'))
    try:
        if(""==method_routing_id): # if method_routing_id=="". we will create a new method routing .
            urlpath = '/management/method_routings'
            result = api.post(urlpath, payload=payload)
        else: # if method_routing_id not empty. we will update the current method routing ..
            urlpath = '/management/method_routings/{}'.format(method_routing_id)
            result = api.put(urlpath, payload=payload)
    except APIError as err:
        error_once_only(request, APIError(Exception("OBP-API server is not running or do not response properly. "
                                                     "Please check OBP-API server.   Details: " + str(err))))
    except Exception as err:
        error_once_only(request, "Unknown Error. Details: " + str(err))
    if 'code' in result and result['code'] >= 400:
        error_once_only(request, result['message'])
        msg = 'Submission successfully!'
        messages.success(request, msg)
    return JsonResponse({'state': True})


@csrf_exempt
def methodrouting_delete(request):
    method_routing_id = request.POST.get('method_routing_id')

    api = API(request.session.get('obp'))

    try:
        urlpath = '/management/method_routings/{}'.format(method_routing_id)
        result = api.delete(urlpath)
    except APIError as err:
        error_once_only(request, APIError(Exception("OBP-API server is not running or do not response properly. "
                                                     "Please check OBP-API server.   Details: " + str(err))))
    except Exception as err:
        error_once_only(request, "Unknown Error. Details: " + str(err))
    if 'code' in result and result['code'] >= 400:
        error_once_only(request, result['message'])
        msg = 'Submission successfully!'
        messages.success(request, msg)
    return JsonResponse({'state': True})