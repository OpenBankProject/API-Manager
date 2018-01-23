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



class IndexView(LoginRequiredMixin, TemplateView):
    """Index view for entitlement requests"""
    template_name = "entitlementrequests/index.html"

    def scrub(self, entitlement_requests):
        """Scrubs data in the given entitlement requests to adher to certain formats"""
        for entitlement_request in entitlement_requests:
            entitlement_request['created'] = datetime.strptime(
                entitlement_request['created'], settings.API_DATETIMEFORMAT)
        return entitlement_requests

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        entitlement_requests = []
        api = API(self.request.session.get('obp'))
        try:
            urlpath = '/entitlement-requests'
            entitlement_requests = api.get(urlpath)
            entitlement_requests = entitlement_requests['entitlement_requests']
            entitlement_requests = FilterTime(context, self.request.GET, 'created') \
                .apply(entitlement_requests)
            entitlement_requests = self.scrub(entitlement_requests)
        except APIError as err:
            messages.error(self.request, err)

        context.update({
            'entitlementrequests': entitlement_requests,
        })
        return context

class DeleteEntitlementRequest(LoginRequiredMixin, View):
    """View to delete an entitlement"""

    def post(self, request, *args, **kwargs):
        """Deletes entitlement from API"""
        api = API(self.request.session.get('obp'))
        try:
            urlpath = '/entitlement-requests/{}'.format(
                kwargs['entitlement_request_id'])
            api.delete(urlpath)
            msg = 'Entitlement Request with role {} has been deleted.'.format(
                request.POST.get('role_name', '<undefined>'))
            messages.success(request, msg)
        except APIError as err:
            messages.error(request, err)

        redirect_url = request.POST.get('next', reverse('entitlementrequests-index'))
        return HttpResponseRedirect(redirect_url)