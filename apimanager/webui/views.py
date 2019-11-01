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
    web_ui_props_name = request.POST.get('web_ui_props_name')
    web_ui_props_value = request.POST.get('web_ui_props_value')

    payload = {
        'name': web_ui_props_name,
        'value': web_ui_props_value
    }

    response = __send_request(request, '/management/webui_props', 'post', payload)
    status_code = response['code']

    errors = [str(m.message) for m in messages.get_messages(request)]
    response = JsonResponse({'code': status_code, 'errors': errors, 'web_ui_props_id': response['result']['web_ui_props_id']})
    response.status_code = status_code
    return response

@csrf_exempt
def webui_delete(request):
    web_ui_props_id = request.POST.get('web_ui_props_id')
    web_ui_props_name = request.POST.get('web_ui_props_name')
    if web_ui_props_id == 'default' or web_ui_props_id == ''or web_ui_props_id is None:
        status_code = 200
    else:
        status_code = __send_request(request, '/management/webui_props/' + web_ui_props_id, 'delete')['code']
    default_value = ''
    if 200 <= status_code <= 299:
        all_webui = __send_request(request, '/management/webui_props?active=true', 'get')
        status_code = all_webui['code']
        for v in all_webui['result']['webui_props']:
            if v['name'] == web_ui_props_name:
                default_value = v['value']
                break

    errors = [str(m.message) for m in messages.get_messages(request)]
    response = JsonResponse({'code': status_code, 'errors': errors, 'default_value': default_value})
    response.status_code = status_code
    return response

def __send_request(request, url, method_name, payload = None):
    api = API(request.session.get('obp'))
    code = 200
    try:
        if payload:
            result = getattr(api, method_name)(url, payload=payload)
        else:
            result = getattr(api, method_name)(url)
    except APIError as err:
        code = 500
        error_once_only(request, APIError(Exception("The OBP-API server is not running or does not respond properly."
                                                    "Please check OBP-API server.   Details: " + str(err))))
    except Exception as err:
        code = 500
        error_once_only(request, "Unknown Error. Details: " + str(err))

    if 'code' in result and result['code'] >= 400:
        code = int(result['code'])
        error_once_only(request, result['message'])

    return {'code': code, 'result': result}
