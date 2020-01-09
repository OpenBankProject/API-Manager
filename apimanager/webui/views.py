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
from utils.ErrorHandler import exception_handle, error_once_only

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
                #print(response)
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

@exception_handle
@csrf_exempt
def webui_save(request):
    web_ui_props_name = request.POST.get('web_ui_props_name')
    web_ui_props_value = request.POST.get('web_ui_props_value')

    payload = {
        'name': web_ui_props_name,
        'value': web_ui_props_value
    }
    api = API(request.session.get('obp'))
    urlpath = '/management/webui_props'
    response = api.post(urlpath, payload=payload)
    
    return response

@exception_handle
@csrf_exempt
def webui_delete(request):
    web_ui_props_id = request.POST.get('web_ui_props_id')
    web_ui_props_name = request.POST.get('web_ui_props_name')
    if web_ui_props_id == 'default' or web_ui_props_id == '' or web_ui_props_id is None:
        return {'code':403,'message':'Cann\'t delete web_ui_props_id default'}
    else:
        api = API(request.session.get('obp'))
        urlpath = '/management/webui_props/{}'.format(web_ui_props_id)
        result = api.delete(urlpath)
        print(result)
        return result
