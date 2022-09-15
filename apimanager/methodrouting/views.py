# -*- coding: utf-8 -*-
"""
Views of config app
"""

import json

from django.conf import settings
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import FormView

from base.utils import error_once_only, exception_handle
from obp.api import API, APIError
from .forms import MethodRoutingForm
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt


class IndexView(LoginRequiredMixin, FormView):
    """Index view for config"""
    template_name = "methodrouting/index.html"
    form_class = MethodRoutingForm
    success_url = reverse_lazy('methodrouting-index')

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        api = API(self.request.session.get('obp'))
        urlpath = '/management/method_routings?active=true'
        method_routings =[]
        try:
            response = api.get(urlpath)
            if 'code' in response and response['code'] >= 400:
                error_once_only(self.request, response['message'])
            else:
                method_routings=response['method_routings']
        except APIError as err:
            messages.error(self.request, err)
        except BaseException as err:
            error_once_only(self.request, (Exception("Unknown Error. Details:" + str(err))))
        else:
            for i in range(len(method_routings)):
                #if the parameters are empty, we provide the example value.
                if(str(method_routings[i]['parameters']).find("key") == -1):
                    method_routings[i]['parameters'] = json.dumps([{
                        "key":"url",
                        "value":"http://example.com/xxx"
                    }], sort_keys=False)
                else:
                    method_routings[i]['parameters'] = json.dumps(method_routings[i]['parameters'], sort_keys=False)

            if(str(settings.API_ROOT).find("127.0.0.1") == -1):
                methodSwaggerUrl = '{}/message-docs?connector=stored_procedure_vDec2019#'.format(settings.API_HOST.replace(".openbankproject.", "-explorer.openbankproject."))
            else:
                methodSwaggerUrl = "http://127.0.0.1:8082/message-docs?connector=stored_procedure_vDec2019#"
            
            context.update({
                'method_routings': method_routings,
                "methodSwaggerUrl": methodSwaggerUrl
            })
        return context

@exception_handle
@csrf_exempt
def methodrouting_save(request):
    method_name = request.POST.get('method_name')
    connector_name = request.POST.get('connector_name')
    bank_id_pattern = request.POST.get('bank_id_pattern')
    is_bank_id_exact_match = request.POST.get('is_bank_id_exact_match')
    parameters = request.POST.get('parameters')
    method_routing_id = request.POST.get('method_routing_id')
    parameters_Json_editor = request.POST.get('parameters_Json_editor')
    #from sonarcloud: Dynamic code execution should not be vulnerable to injection attacks
    exec("import json" % json.loads(parameters_Json_editor)) # Compliant; module is safely cast to json object
    payload = {
        'method_name' : method_name,
        'connector_name': connector_name,
        'is_bank_id_exact_match': (is_bank_id_exact_match=="True"),
        'bank_id_pattern':bank_id_pattern,
        'parameters':json.loads(parameters_Json_editor),
        'method_routing_id':method_routing_id
    }

    api = API(request.session.get('obp'))
    if(""==method_routing_id): # if method_routing_id=="". we will create a new method routing .
        urlpath = '/management/method_routings'
        result = api.post(urlpath, payload=payload)
    else: # if method_routing_id not empty. we will update the current method routing ..
        urlpath = '/management/method_routings/{}'.format(method_routing_id)
        result = api.put(urlpath, payload=payload)
    return result


@exception_handle
@csrf_exempt
def methodrouting_delete(request):
    method_routing_id = request.POST.get('method_routing_id')

    api = API(request.session.get('obp'))

    urlpath = '/management/method_routings/{}'.format(method_routing_id)
    result = api.delete(urlpath)
    return result