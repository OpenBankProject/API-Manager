# -*- coding: utf-8 -*-
"""
Views of metrics app
"""

import json
import hashlib
import operator

from datetime import datetime

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from base.api import api, APIError



def get_random_color(to_hash):
    hashed = str(int(hashlib.md5(to_hash.encode('utf-8')).hexdigest(), 16))
    r = int(hashed[0:3]) % 255
    b = int(hashed[3:6]) % 255
    g = int(hashed[6:9]) % 255
    return 'rgba({}, {}, {}, 0.3)'.format(r, g, b)



def get_barchart_data(metrics, fieldname):
    """
    Gets bar chart data compatible with Chart.js from the field with given
    fieldname in given metrics
    """
    border_color = 'rgba(0, 0, 0, 1)'
    data = {
        'labels': [],
        'data': [],
        'backgroundColor': [],
        'borderColor': [],
    }
    items = {}
    for metric in metrics:
        if not metric[fieldname]:
            continue
        if metric[fieldname] in items:
            items[metric[fieldname]] += 1
        else:
            items[metric[fieldname]] = 1
    sorted_items = sorted(
            items.items(), key=operator.itemgetter(1), reverse=True)
    for item in sorted_items:
        data['labels'].append(item[0])
        data['data'].append(item[1])
        data['backgroundColor'].append(get_random_color(item[0]))
        data['borderColor'].append(border_color)
    return data



class IndexView(LoginRequiredMixin, TemplateView):
    """Index view for metrics"""
    template_name = "metrics/index.html"

    def scrub(self, metrics):
        """Scrubs data in the given consumers to adher to certain formats"""
        for metric in metrics:
            metric['date'] = datetime.strptime(
                metric['date'], settings.API_DATETIMEFORMAT)
        return metrics


    def get_params(self, request_get):
        """
        API treats empty parameters as actual values, so we have to filter
        them out
        """
        querydict = request_get.copy()
        keys = list(querydict.keys())
        for key in keys:
            if not querydict[key]:
                querydict.pop(key)
        return querydict.urlencode()


    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        metrics = []
        params = self.get_params(self.request.GET)
        try:
            urlpath = '/management/metrics?{}'.format(params)
            metrics = api.get(self.request, urlpath)
            metrics = self.scrub(metrics['metrics'])
        except APIError as err:
            messages.error(self.request, err)

        context.update({
            'metrics': metrics,
            'barchart_data': json.dumps({})
        })
        return context



class SummaryPartialFunctionView(IndexView):
    template_name = "metrics/summary_partial_function.html"

    def get_context_data(self, **kwargs):
        context = super(SummaryPartialFunctionView, self).get_context_data(
            **kwargs)
        barchart_data = json.dumps(get_barchart_data(
            context['metrics'], 'implemented_by_partial_function'))

        context.update({
            'barchart_data': barchart_data,
        })
        return context
