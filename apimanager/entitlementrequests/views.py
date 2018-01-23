# -*- coding: utf-8 -*-
"""
Views of entitlement requests app
"""

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, RedirectView
from obp.api import API, APIError


class IndexView(LoginRequiredMixin, TemplateView):
    """Index view for entitlement requests"""
    template_name = "entitlementrequests/index.html"

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        entitlement_requests = []
        api = API(self.request.session.get('obp'))
        try:
            urlpath = '/entitlement-requests'
            entitlement_requests = api.get(urlpath)
        except APIError as err:
            messages.error(self.request, err)

        sorted_entitlement_requests = entitlement_requests['entitlement_requests']
        context.update({
            'entitlementrequests': sorted_entitlement_requests,
        })
        return context
