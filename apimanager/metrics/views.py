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
from django.views.generic import FormView, TemplateView
from django.utils.http import urlquote

from obp.api import API, APIError

from .forms import APIMetricsForm, ConnectorMetricsForm


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


class MetricsView(LoginRequiredMixin, TemplateView):
    """View for metrics (sort of abstract base class)"""
    form_class = None
    template_name = None
    api_urlpath = None

    def get_form(self):
        """
        Get bound form either from request.GET or initials
        We need a bound form because we already send a request to the API
        without user intervention on initial request
        """
        if self.request.GET:
            data = self.request.GET
        else:
            fields = self.form_class.declared_fields
            data = {}
            for name, field in fields.items():
                if field.initial:
                    data[name] = field.initial
        form = self.form_class(data)
        return form

    def to_django(self, metrics):
        """
        Convert metrics data from API to format understood by Django
        - Make datetime out of string in field 'date'
        """
        for metric in metrics:
            metric['date'] = datetime.strptime(
                metric['date'], settings.API_DATETIMEFORMAT)
        return metrics

    def to_api(self, cleaned_data):
        """
        Convert form data from Django to format understood by API
        - API treats empty parameters as actual values, so we have to remove
        them
        - Need to convert datetimes into required format
        """
        params = []
        for name, value in cleaned_data.items():
            # Maybe we should define the API format as Django format to not
            # have to convert in places like this?
            if value.__class__.__name__ == 'datetime':
                value = value.strftime(settings.API_DATEFORMAT)
            if value:
                # API does not like quoted data
                params.append('{}={}'.format(name, value))
        params = '&'.join(params)
        return params

    def get_metrics(self, cleaned_data):
        """
        Gets the metrics from the API, using given cleaned form data.
        """
        metrics = []
        params = self.to_api(cleaned_data)
        urlpath = '{}?{}'.format(self.api_urlpath, params)
        api = API(self.request.session.get('obp'))
        try:
            metrics = api.get(urlpath)
            metrics = self.to_django(metrics['metrics'])
        except APIError as err:
            messages.error(self.request, err)
        return metrics

    def get_context_data(self, **kwargs):
        context = super(MetricsView, self).get_context_data(**kwargs)
        metrics = []
        form = self.get_form()
        if form.is_valid():
            metrics = self.get_metrics(form.cleaned_data)
        context.update({
            'metrics': metrics,
            'form': form,
        })
        return context


class APIMetricsView(MetricsView):
    """View for API metrics"""
    form_class = APIMetricsForm
    template_name = 'metrics/api.html'
    api_urlpath = '/management/metrics'


class APISummaryPartialFunctionView(APIMetricsView):
    template_name = 'metrics/api_summary_partial_function.html'

    def get_context_data(self, **kwargs):
        context = super(APISummaryPartialFunctionView, self).get_context_data(
            **kwargs)
        barchart_data = json.dumps(get_barchart_data(
            context['metrics'], 'implemented_by_partial_function'))

        context.update({
            'barchart_data': barchart_data,
        })
        return context


class ConnectorMetricsView(MetricsView):
    """View for connector metrics"""
    form_class = ConnectorMetricsForm
    template_name = 'metrics/connector.html'
    api_urlpath = '/management/connector/metrics'
