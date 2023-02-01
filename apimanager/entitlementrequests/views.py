# -*- coding: utf-8 -*-
"""
Views of entitlement requests app
"""

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, RedirectView, View
from obp.api import API, APIError
from base.filters import BaseFilter, FilterTime
from datetime import datetime
from django.conf import settings
from django.urls import reverse
from django.http import HttpResponseRedirect
from apimanager.settings import UNDEFINED



class IndexView(LoginRequiredMixin, TemplateView):
    """Index view for entitlement requests"""
    template_name = "entitlementrequests/index.html"

    def scrub(self, entitlement_requests):
        """Scrubs data in the given entitlement requests to adher to certain formats"""
        for entitlement_request in entitlement_requests:
            entitlement_request['created'] = datetime.strptime(
                entitlement_request['created'], settings.API_DATE_TIME_FORMAT)
        return entitlement_requests

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        entitlement_requests = []
        api = API(self.request.session.get('obp'))
        try:
            urlpath = '/entitlement-requests'
            entitlement_requests = api.get(urlpath)
            if 'code' in entitlement_requests and entitlement_requests['code']>=400:
                messages.error(self.request, entitlement_requests['message'])
                entitlement_requests = []
            else:
                entitlement_requests = entitlement_requests['entitlement_requests']
                entitlement_requests = FilterTime(context, self.request.GET, 'created') \
                    .apply(entitlement_requests)
                entitlement_requests = self.scrub(entitlement_requests)
                entitlement_requests = sorted(entitlement_requests, key=lambda k: k['created'], reverse=True)
        except APIError as err:
            messages.error(self.request, err)
        except Exception as err:
            messages.error(self.request, err)

        context.update({
            'entitlementrequests': entitlement_requests,
        })
        return context

class RejectEntitlementRequest(LoginRequiredMixin, View):
    """View to delete an entitlement"""

    def post(self, request, *args, **kwargs):
        """Deletes entitlement from API"""
        api = API(self.request.session.get('obp'))
        try:
            urlpath = '/entitlement-requests/{}'.format(
                kwargs['entitlement_request_id'])
            response = api.delete(urlpath)
            if 'code' in response and response['code'] >= 400:
                messages.error(self.request, response['message'])
            else:
                msg = 'Entitlement Request with role {} has been deleted.'.format(
                    request.POST.get('role_name', UNDEFINED))
                messages.success(request, msg)
        except APIError as err:
            messages.error(request, err)
        except Exception as err:
            messages.error(self.request, err)

        return HttpResponseRedirect(reverse('entitlementrequests-index'))


class AcceptEntitlementRequest(LoginRequiredMixin, View):
    """View to add entitlement and delete an entitlement request"""

    def post(self, request, *args, **kwargs):
        """Deletes entitlement request from API"""
        api = API(self.request.session.get('obp'))

        try:
            urlpath = '/users/{}/entitlements'.format(kwargs['user_id'])
            payload = {
                'bank_id': request.POST.get('bank_id', UNDEFINED),
                'role_name': request.POST.get('role_name', UNDEFINED),
            }
            response = api.post(urlpath, payload=payload)
            if 'code' in response and response['code'] >= 400:
                messages.error(self.request, response['message'])
            else:
                msg = 'Entitlement with role {} has been added.'.format(request.POST.get('role_name', UNDEFINED))
                messages.success(request, msg)
        except APIError as err:
            messages.error(request, err)
        except Exception as err:
            messages.error(self.request, err)

        try:
            urlpath = '/entitlement-requests/{}'.format(request.POST.get('entitlement_request_id', UNDEFINED))
            response = api.delete(urlpath)
            if 'code' in response and response['code'] >= 400:
                messages.error(self.request, response['message'])
            else:
                msg = 'Entitlement Request with role {} has been deleted.'.format(
                    request.POST.get('role_name', UNDEFINED))
                messages.success(request, msg)
        except APIError as err:
            messages.error(request, err)
        except Exception as err:
            messages.error(self.request, err)

        return HttpResponseRedirect(reverse('entitlementrequests-index'))
