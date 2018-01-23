# -*- coding: utf-8 -*-
"""
Views of entitlement requests app
"""

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, RedirectView
from obp.api import API, APIError
from base.filters import BaseFilter, FilterTime
from datetime import datetime
from django.conf import settings



class IndexView(LoginRequiredMixin, TemplateView):
    """Index view for entitlement requests"""
    template_name = "entitlementrequests/index.html"

    def scrub(self, entitlement_requests):
        """Scrubs data in the given consumers to adher to certain formats"""
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
