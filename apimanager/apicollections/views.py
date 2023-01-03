# -*- coding: utf-8 -*-
"""
Views of API Collection app
"""

import json
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.views.generic import FormView
from obp.api import API, APIError
from django.urls import reverse, reverse_lazy
from base.utils import exception_handle, error_once_only
from .forms import ApiCollectionsForm, ApiCollectionEndpointsForm
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

class IndexView(LoginRequiredMixin, FormView):
    """Index view for API Collection"""
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
                for locale in api_collections:
                    locale["collection_on_api_explorer_url"] = f"{settings.API_EXPLORER}/?api-collection-id={locale['api_collection_id']}"
        except APIError as err:
            messages.error(self.request, err)
        except Exception as err:
            error_once_only(self.request, err)
        else:
            # set the default endpoint there, the first item will be the new endpoint.
            default_api_endpoint = {
                "api_collection_name": "Customer",
                "is_sharable": True,
                "description":"Describe the purpose of the collection"
            }
            api_collections.insert(0,json.dumps(default_api_endpoint))
            
            context.update({
                'api_collections': api_collections
            })
        return context

class DetailView(LoginRequiredMixin, FormView):
    """Index view for config"""
    template_name = "apicollections/detail.html"
    form_class = ApiCollectionEndpointsForm
    success_url = reverse_lazy('my-api-collection-detail')
    
    def form_valid(self, form):
        """Posts api collection endpoint data to API"""
        try:
            data = form.cleaned_data
            api = API(self.request.session.get('obp'))
            api_collection_id = super(DetailView, self).get_context_data()['view'].kwargs['api_collection_id']
        
            urlpath = '/my/api-collection-ids/{}/api-collection-endpoints'.format(api_collection_id) 
            payload = {
                'operation_id': data['operation_id']
            }
            api_collection_endpoint = api.post(urlpath, payload=payload)
        except APIError as err:
            messages.error(self.request, err)
            return super(DetailView, self).form_invalid(form)
        except Exception as err:
            error_once_only(self.request, err)
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
        api_collection_id = context['view'].kwargs['api_collection_id']

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
            messages.error(self.request, result['message'])
        except Exception as err:
            error_once_only(self.request, err)
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
            get_api_collection_by_id_url = "/my/api-collections/{}".format(kwargs["api_collection_id"])
            result = api.get(get_api_collection_by_id_url)
            urlpath = '/my/api-collections/{}/api-collection-endpoints/{}'.format(kwargs['api_collection_name'],kwargs['operation_id'])
            result = api.delete(urlpath)
            if result is not None and 'code' in result and result['code']>=400:
                messages.error(request, result['message'])
            else:
                msg = 'Operation Id {} has been deleted.'.format(kwargs['operation_id'])
                messages.success(request, msg)
        except APIError as err:
            messages.error(request, err)
        except Exception as err:
            messages.error(self.request, 'Unknown Error', err)
        redirect_url = reverse('my-api-collection-detail',kwargs={"api_collection_id":kwargs['api_collection_id']})
        return HttpResponseRedirect(redirect_url)
    
@exception_handle
@csrf_exempt
def apicollections_save(request):
    api = API(request.session.get('obp'))
    urlpath = '/my/api-collections'
    payload = {
        'api_collection_name': request.POST.get('api_collection_name').strip(),
        'is_sharable': bool(request.POST.get('api_collection_is_sharable')),
        'description': request.POST.get('api_collection_description').strip()
    }
    result = api.post(urlpath, payload = payload)
    return result

@exception_handle
@csrf_exempt
def connectormethod_update(request):
    connector_method_id = request.POST.get('api_collection_id').strip()
    urlpath = '/management/api-collection/{}'.format(connector_method_id) #TODO : Wainting for URL
    api = API(request.session.get('obp'))
    #Update Endpoint Payload define
    payload = {
        'api_collection_is_sharable': request.POST.get('api_collection_is_sharable'),
        'method_body': request.POST.get('api_collection_method_body_update').strip()
    }
    result = api.put(urlpath, payload=payload)
    return result



@exception_handle
@csrf_exempt
def apicollections_delete(request):
    api_collection_id = request.POST.get('api_collection_id').strip()

    api = API(request.session.get('obp'))
    urlpath = '/my/api-collections/{}'.format(api_collection_id)
    result = api.delete(urlpath)
    return result
