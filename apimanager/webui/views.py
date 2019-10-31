# -*- coding: utf-8 -*-
"""
Views of config app
"""

import json

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import FormView
from obp.api import API, APIError
from django.http import JsonResponse
from .forms import WebuiForm
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
    template_name = "webui/index.html"
    form_class = WebuiForm
    success_url = reverse_lazy('webui-index')

    def dispatch(self, request, *args, **kwargs):
        self.api = API(request.session.get('obp'))
        return super(IndexView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        api = API(self.request.session.get('obp'))
        urlpath = '/management/webui_props?active=true'

        try:
            response = api.get(urlpath)
            if 'code' in response and response['code'] >= 400:
                messages.error(self.request, response['message'])
                context.update({'webui_props': []})
            else:
                # Here is response of getWebuiProps.
                # {
                #     "webui_props": [
                #         {
                #             "name": "webui_header_logo_left_url ",
                #             "value": " /media/images/logo.png",
                #             "web_ui_props_id": "default"
                #         }
                #     ]
                # }
                context.update(response)
        except APIError as err:
            messages.error(self.request, Exception("The OBP-API server is not running or does not respond properly."
                                               "Please check OBP-API server.    "
                                               "Details: " + str(err)))
        except BaseException as err:
            messages.error(self.request, (Exception("Unknown Error. Details:" + str(err))))
        return context

    def get_form(self, *args, **kwargs):
        form = super(IndexView, self).get_form(*args, **kwargs)
        return form

@csrf_exempt
def webui_save(request):
    webui_props_name = request.POST.get('webui_props_name')
    webui_props_value = request.POST.get('webui_props_value')

    payload = {
        'name': webui_props_name,
        'value': webui_props_value
    }

    api = API(request.session.get('obp'))
    try:
        urlpath = '/management/webui_props'
        result = api.post(urlpath, payload=payload)
    except APIError as err:
        error_once_only(request, APIError(Exception("The OBP-API server is not running or does not respond properly."
                                                    "Please check OBP-API server.   Details: " + str(err))))
    except Exception as err:
        error_once_only(request, "Unknown Error. Details: " + str(err))
    if 'code' in result and result['code'] >= 400:
        error_once_only(request, result['message'])
        msg = 'Submit successfully!'
        messages.success(request, msg)
    return JsonResponse({'state': True})

@csrf_exempt
def webui_delete(request):
    web_ui_props_id = request.POST.get('web_ui_props_id')

    api = API(request.session.get('obp'))
    try:
        urlpath = '/management/webui_props/{}'.format(web_ui_props_id)
        result = api.delete(urlpath)
    except APIError as err:
        error_once_only(request, APIError(Exception("The OBP-API server is not running or does not respond properly."
                                                    "Please check OBP-API server.   Details: " + str(err))))
    except Exception as err:
        error_once_only(request, "Unknown Error. Details: " + str(err))
    if 'code' in result and result['code'] >= 400:
        error_once_only(request, result['message'])
        msg = 'Submit successfully!'
        messages.success(request, msg)
    return JsonResponse({'state': True})