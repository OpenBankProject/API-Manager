# -*- coding: utf-8 -*-
"""
Views of config app
"""

import json
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.views.generic import FormView
from obp.api import API, APIError
from django.urls import reverse, reverse_lazy
from base.utils import exception_handle, error_once_only
from .forms import ConnectorMethodForm, ConnectorMethodEndpointForm
from django.views.decorators.csrf import csrf_exempt


class IndexView(LoginRequiredMixin, FormView):
    """Index view for Connector Methods"""
    template_name = "connectormethod/index.html"
    form_class = ConnectorMethodForm
    success_url = reverse_lazy('connectormethod-index')
    def dispatch(self, request, *args, **kwargs):
            self.api = API(request.session.get('obp'))
            return super(IndexView, self).dispatch(request, *args, **kwargs)

    def get_form(self, *args, **kwargs):
        form = super(IndexView, self).get_form(*args, **kwargs)
        # Cannot add api in constructor: super complains about unknown kwarg
        form.api = self.api
        fields = form.fields
        try:
            fields['is_accessible'].choices = [('',_('Choose...')),(Scala, Scala), (Java, Java), (JavaScript, JavaScript)]
        except APIError as err:
            messages.error(self.request, err)
        except Exception as err:
            messages.error(self.request, err)

        return form
    def form_valid(self, form):
        try:
            data = form.cleaned_data
            urlpath = '/management/connector-methods'
            payload ={
                "connector_method_id": data["connector_method_id"],
                "method_name": data["method_name"],
                "programming_lang": data["programming_lang"] if data["programming_lang"]!="" else "false",
                "method_body": data["method_body"],
            }
            result = self.api.post(urlpath, payload=payload)
        except APIError as err:
            messages.error(self.request, "Unknown Error")
            return super(IndexView, self).form_invalid(form)
        except Exception as err:
            messages.error(self.request, "Unknown Error")
            return super(IndexView, self).form_invalid(form)
        if 'code' in result and result['code']>=400:
            messages.error(self.request, result['message'])
            return super(IndexView, self).form_valid(form)
        msg = 'Connector Method has been created successfully!'
        messages.success(self.request, msg)
        return super(IndexView, self).form_valid(form)

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
            messages.error(self.request, err)
            #error_once_only(self.request, Exception("OBP-API server is not running or do not response properly. "
            #                                       "Please check OBP-API server.    "
            #                                       "Details: " + str(err)))
        except BaseException as err:
            messages.error(self.request, 'KeyError: {}'.format(err))
            #error_once_only(self.request, (Exception("Unknown Error. Details:" + str(err))))
        else:
            # set the default endpoint there, the first item will be the new endpoint.
            default_api_endpoint = {
                "connectormethod": "method_name",
                "is_sharable": True,
                "description":"Describe the purpose of the collection"
            }
            connectormethod.insert(0,json.dumps(default_api_endpoint))
            
            context.update({
                'connectormethods': connectormethod
            })
        return context

class DetailView(LoginRequiredMixin, FormView):
    """Index view for config"""
    template_name = "connectormethod/detail.html"
    form_class = ConnectorMethodEndpointForm
    success_url = reverse_lazy('connector_detail')
    
    def form_valid(self, form):
        """Posts api collection endpoint data to API"""
        try:
            data = form.cleaned_data
            api = API(self.request.session.get('obp'))
            connectormethod_id = super(DetailView, self).get_context_data()['view'].kwargs['connectormethod_id']
        
            urlpath = '/my/api-collection-ids/{}/api-collection-endpoints'.format(api_collection_id) 
            payload = {
                'operation_id': data['operation_id']
            }
            api_collection_endpoint = api.post(urlpath, payload=payload)
        except APIError as err:
            messages.error(self.request, err)
            return super(DetailView, self).form_invalid(form)
        except:
            messages.error(self.request, 'Unknown Error')
            return super(DetailView, self).form_invalid(form)
        if 'code' in api_collection_endpoint and api_collection_endpoint['code']>=400:
            messages.error(self.request, api_collection_endpoint['message'])
            return super(DetailView, self).form_invalid(form)
        else:
            msg = 'Operation Id {} has been added.'.format(data['operation_id'])
            messages.success(self.request, msg)
            self.success_url = self.request.path
            return super(DetailView, self).form_valid(form)
        
    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        connectormethod_id = context['view'].kwargs['connectormethod_id']

        api = API(self.request.session.get('obp'))
        urlpath = '/my/api-collection-ids/{}/api-collection-endpoints'.format(api_collection_id)
        api_collection_endpoints =[]
        try:
            response = api.get(urlpath)
            if 'code' in response and response['code'] >= 400:
                error_once_only(self.request, response['message'])
            else:
                api_collection_endpoints=response['api_collection_endpoints']
        except APIError as err:
            error_once_only(self.request, Exception("OBP-API server is not running or do not response properly. "
                                                   "Please check OBP-API server.    "
                                                   "Details: " + str(err)))
        except BaseException as err:
            error_once_only(self.request, (Exception("Unknown Error. Details:" + str(err))))
        else:
            context.update({
                'api_collection_endpoints': api_collection_endpoints,
                'api_collection_id': api_collection_id
            })
        return context

class DeleteCollectionEndpointView(LoginRequiredMixin, FormView):
    """View to delete an api collection endpoint"""
    def post(self, request, *args, **kwargs):
        """Deletes api collection endpoint from API"""
        api = API(self.request.session.get('obp'))
        try:
            urlpath = '/my/api-collections-ids/{}/api-collection-endpoints/{}'\
                .format(kwargs['api_collection_id'],kwargs['operation_id'])
            result = api.delete(urlpath)
            if result is not None and 'code' in result and result['code']>=400:
                messages.error(request, result['message'])
            else:
                msg = 'Operation Id {} has been deleted.'.format(kwargs['operation_id'])
                messages.success(request, msg)
        except APIError as err:
            messages.error(request, err)
        except:
            messages.error(self.request, 'Unknown Error')

        redirect_url = reverse('my-api-collection-detail',kwargs={"api_collection_id":kwargs['api_collection_id']})
        return HttpResponseRedirect(redirect_url)
    
@exception_handle
@csrf_exempt
def connectormethod_save(request):
    api = API(request.session.get('obp'))
    urlpath = '/my/connectormethod'
    payload = {
        'api_collection_name': request.POST.get('api_collection_name').strip(),
        'is_sharable': bool(request.POST.get('api_collection_is_sharable')),
        'description': request.POST.get('api_collection_description').strip()
    }
    result = api.post(urlpath, payload = payload)
    return result


@exception_handle
@csrf_exempt
def apicollections_delete(request):
    api_collection_id = request.POST.get('api_collection_id').strip()

    api = API(request.session.get('obp'))
    urlpath = '/my/api-collections/{}'.format(api_collection_id)
    result = api.delete(urlpath)
    return result
