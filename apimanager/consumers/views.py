# -*- coding: utf-8 -*-
import json
from copy import deepcopy
from datetime import datetime

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import TemplateView, RedirectView

from base.filters import BaseFilter, FilterTime
from base.utils import json_serial, api_get, api_put, api_post



class FilterAppType(BaseFilter):
    filter_type = 'apptype'

    def _apply(self, data, filter_value):
        filtered = [x for x in data if x['appType'] == filter_value]
        return filtered


class FilterEnabled(BaseFilter):
    filter_type = 'enabled'

    def _apply(self, data, filter_value):
        enabled = filter_value in ['true']
        filtered = [x for x in data if x['enabled'] == enabled]
        return filtered



class IndexView(LoginRequiredMixin, TemplateView):
    template_name = "consumers/index.html"

    def scrub(self, data):
        for consumer in data:
            consumer['created'] = datetime.strptime(
                consumer['created'], settings.API_DATETIMEFORMAT)
        return data

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        filtered = []
        urlpath = '/management/consumers'
        consumers = api_get(self.request, urlpath)

        if not isinstance(consumers, dict):
            messages.error(self.request, consumers)
        elif 'error' in consumers:
            messages.error(self.request, consumers['error'])
        else:
            filtered = FilterEnabled(context, self.request.GET)\
                .apply(consumers['list'])
            filtered = FilterAppType(context, self.request.GET)\
                .apply(filtered)
            filtered = FilterTime(context, self.request.GET, 'created')\
                .apply(filtered)
            filtered = self.scrub(filtered)

        context.update({
            'consumers': filtered,
            'consumers_json': json.dumps(filtered, default=json_serial),
            'statistics': {
                'consumers_num': len(filtered),
            },
        })
        return context



class DetailView(LoginRequiredMixin, TemplateView):
    template_name = "consumers/detail.html"

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        urlpath = '/management/consumers/{}'.format(kwargs['consumer_id'])
        consumer = api_get(self.request, urlpath)
        
        if not isinstance(consumer, dict):
            messages.error(self.request, consumer)
        elif 'error' in consumer:
            messages.error(self.request, consumer['error'])
        else:
            consumer['created'] = datetime.strptime(
                consumer['created'], settings.API_DATETIMEFORMAT)

        context.update({
            'consumer': consumer,
        })
        return context



class EnableDisableView(LoginRequiredMixin, RedirectView):
    def get_redirect_url(self,*args, **kwargs):
        urlpath = '/management/consumers/{}'.format(kwargs['consumer_id'])
        payload = {'enabled': self.enabled}
        result = api_put(self.request, urlpath, payload)
        if 'error' in result:
            messages.error(self.request, result['error'])
        else:
            messages.success(self.request, self.success)
        urlpath = self.request.POST.get('next', reverse('consumers-index'))
        query = self.request.GET.urlencode()
        redirect_url = '{}?{}'.format(urlpath, query)
        return redirect_url



class EnableView(EnableDisableView):
    enabled = True
    success = "Consumer has been enabled."


class DisableView(EnableDisableView):
    enabled = False
    success = "Consumer has been disabled."
