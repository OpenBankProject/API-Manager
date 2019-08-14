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
        webui_props = []
        api = API(self.request.session.get('obp'))
        urlpath = '/management/webui_props?active=true'

        try:
            # response = api.get(urlpath)
            response = json.loads("""{
  "webui_props": [
    {
      "name": "webui_header_logo_left_url ",
      "value": " /media/images/logo.png",
      "web_ui_props_id": "default"
    },
    {
      "name": "webui_header_logo_right_url ",
      "value": "",
      "web_ui_props_id": "default"
    },
    {
      "name": "webui_index_page_about_section_background_image_url ",
      "value": " /media/images/about-background.jpg",
      "web_ui_props_id": "default"
    },
    {
      "name": "webui_top_text",
      "value": "",
      "web_ui_props_id": "default"
    },
    {
      "name": "webui_api_explorer_url ",
      "value": " https://apiexplorer.openbankproject.com",
      "web_ui_props_id": "default"
    },
    {
      "name": "webui_sofi_url ",
      "value": " https://sofi.openbankproject.com",
      "web_ui_props_id": "default"
    },
    {
      "name": "webui_api_manager_url ",
      "value": " https://apimanager.openbankproject.com",
      "web_ui_props_id": "default"
    },
    {
      "name": "webui_api_manager_url ",
      "value": " https://apitester.openbankproject.com",
      "web_ui_props_id": "default"
    },
    {
      "name": "webui_api_documentation_url ",
      "value": " https://github.com/OpenBankProject/OBP-API/wiki",
      "web_ui_props_id": "default"
    },
    {
      "name": "webui_login_page_special_instructions",
      "value": "",
      "web_ui_props_id": "default"
    }
  ]
}""")
        except APIError as err:
            messages.error(self.request, Exception("OBP-API server is not running or do not response properly. "
                                               "Please check OBP-API server.    "
                                               "Details: " + str(err)))
        except BaseException as err:
            messages.error(self.request, (Exception("Unknown Error. Details:" + str(err))))
        else:
            webui_props = response["webui_props"]
            context.update({'webui_props': webui_props})
        return context

    def get_form(self, *args, **kwargs):
        form = super(IndexView, self).get_form(*args, **kwargs)
        return form

    def form_valid(self, form):
        try:
            # TODO, need to be fixed later.
            data = form.cleaned_data
            urlpath = '/management/webui_props'
            payload = {
                "name"  : "1",
                "value" : "2"
            }
            result = self.api.post(urlpath, payload=payload)
        except APIError as err:
            error_once_only(self.request, APIError(Exception("OBP-API server is not running or do not response properly. "
                                     "Please check OBP-API server.   Details: " + str(err))))
            return super(IndexView, self).form_invalid(form)
        except Exception as err:
            error_once_only(self.request, "Unknown Error. Details: "+ str(err))
            return super(IndexView, self).form_invalid(form)
        if 'code' in result and result['code']>=400:
            error_once_only(self.request, result['message'])
            return super(IndexView, self).form_valid(form)
        msg = 'Submission successfully!'
        messages.success(self.request, msg)
        return super(IndexView, self).form_valid(form)

def webui_save(request):
    return JsonResponse({'state': True})