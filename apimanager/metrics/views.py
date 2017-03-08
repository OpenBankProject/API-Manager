# -*- coding: utf-8 -*-
"""
Views of metrics app
"""

from datetime import datetime

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from base.api import api, APIError



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
        })
        return context
