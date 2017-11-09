# -*- coding: utf-8 -*-
"""
Views of consumers app
"""

from datetime import datetime

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import TemplateView, RedirectView

from obp.api import API, APIError
from base.filters import BaseFilter, FilterTime


class FilterAppType(BaseFilter):
    """Filter consumers by application type"""
    filter_type = 'app_type'

    def _apply(self, data, filter_value):
        filtered = [x for x in data if x['app_type'] == filter_value]
        return filtered


class FilterEnabled(BaseFilter):
    """Filter consumers by enabled state"""
    filter_type = 'enabled'

    def _apply(self, data, filter_value):
        enabled = filter_value in ['true']
        filtered = [x for x in data if x['enabled'] == enabled]
        return filtered


class IndexView(LoginRequiredMixin, TemplateView):
    """Index view for consumers"""
    template_name = "consumers/index.html"

    def scrub(self, consumers):
        """Scrubs data in the given consumers to adher to certain formats"""
        for consumer in consumers:
            consumer['created'] = datetime.strptime(
                consumer['created'], settings.API_DATETIMEFORMAT)
        return consumers

    def compile_statistics(self, consumers):
        """Compiles a set of statistical values for the given consumers"""
        unique_developer_email = {}
        unique_name = {}
        for consumer in consumers:
            unique_developer_email[consumer['developer_email']] = True
            unique_name[consumer['app_name']] = True
        unique_developer_email = unique_developer_email.keys()
        unique_name = unique_name.keys()
        statistics = {
            'consumers_num': len(consumers),
            'unique_developer_email_num': len(unique_developer_email),
            'unique_name_num': len(unique_name),
        }
        return statistics

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        consumers = []
        api = API(self.request.session.get('obp'))
        try:
            urlpath = '/management/consumers'
            consumers = api.get(urlpath)
            consumers = FilterEnabled(context, self.request.GET)\
                .apply(consumers['list'])
            consumers = FilterAppType(context, self.request.GET)\
                .apply(consumers)
            consumers = FilterTime(context, self.request.GET, 'created')\
                .apply(consumers)
            consumers = self.scrub(consumers)
        except APIError as err:
            messages.error(self.request, err)

        sorted_consumers = sorted(
            consumers, key=lambda consumer: consumer['created'], reverse=True)
        context.update({
            'consumers': sorted_consumers,
            'statistics': self.compile_statistics(consumers),
        })
        return context


class DetailView(LoginRequiredMixin, TemplateView):
    """Detail view for a consumer"""
    template_name = "consumers/detail.html"

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        api = API(self.request.session.get('obp'))

        try:
            urlpath = '/management/consumers/{}'.format(kwargs['consumer_id'])
            consumer = api.get(urlpath)
            consumer['created'] = datetime.strptime(
                consumer['created'], settings.API_DATETIMEFORMAT)
        except APIError as err:
            messages.error(self.request, err)

        context.update({
            'consumer': consumer,
        })
        return context


class EnableDisableView(LoginRequiredMixin, RedirectView):
    """View to enable or disable a consumer"""
    enabled = False
    success = None

    def get_redirect_url(self, *args, **kwargs):
        api = API(self.request.session.get('obp'))
        try:
            urlpath = '/management/consumers/{}'.format(kwargs['consumer_id'])
            payload = {'enabled': self.enabled}
            api.put(urlpath, payload)
            messages.success(self.request, self.success)
        except APIError as err:
            messages.error(self.request, err)

        urlpath = self.request.POST.get('next', reverse('consumers-index'))
        query = self.request.GET.urlencode()
        redirect_url = '{}?{}'.format(urlpath, query)
        return redirect_url


class EnableView(EnableDisableView):
    """View to enable a consumer"""
    enabled = True
    success = "Consumer has been enabled."


class DisableView(EnableDisableView):
    """View to disable a consumer"""
    enabled = False
    success = "Consumer has been disabled."
