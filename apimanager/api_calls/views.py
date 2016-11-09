# -*- coding: utf-8 -*-

import json
from copy import deepcopy
from datetime import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from base.filters import filter_time


CALLS = [
    {
        'method': 'GET',
        'url': '/obp/v2.1.0/banks',
        'code': '200',
        'user': 'Anonymous',
        'when': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'duration': '10',
        'function': 'getBanks',
    },
    {
        'method': 'GET',
        'url': '/obp/v2.1.0/banks',
        'code': '200',
        'user': 'Anonymous',
        'when': '2016-07-03 12:00:00',
        'duration': '10',
        'function': 'getBanks',
    },
    {
        'method': 'GET',
        'url': '/unknown',
        'code': '404',
        'user': 'Anonymous',
        'when': '2015-09-02 10:34:00',
        'duration': '1',
        'function': '',
    },
    {
        'method': 'GET',
        'url': '/obp/v2.1.0/banks',
        'code': '200',
        'user': 'Anonymous',
        'when': '2016-09-12 07:34:00',
        'duration': '10',
        'function': 'getBanks',
    },
    {
        'method': 'GET',
        'url': '/users/current',
        'code': '404',
        'user': 'Anonymous',
        'when': '2016-09-02 10:34:00',
        'duration': '5',
        'function': 'getCurrentUser',
    },
    {
        'method': 'POST',
        'url': '/users/ff3f94f9-bbd6-4cd9-ab78-3701e961eb58/entitlements',
        'code': '500',
        'user': 'shensche',
        'when': '2016-08-10 15:34:00',
        'duration': '23',
        'function': 'getEntitlements',
    },
]



class GroupedView(LoginRequiredMixin, TemplateView):
    template_name = "api_calls/grouped.html"

    def group_functions(self, data):
        functions = {}
        for call in data:
            name = call['function']
            if not name:
                continue
            if not name in functions:
                functions[name] = 1
            else:
                functions[name] += 1
        labels = []
        values = []
        for k in sorted(functions, key=functions.get, reverse=True):
            labels.append(k)
            values.append(functions[k])
        return {'labels': labels, 'values': values}

    def get_context_data(self, **kwargs):
        context = super(GroupedView, self).get_context_data(**kwargs)
        filtered = deepcopy(CALLS)

        filtered = filter_time(self.request, context, filtered, 'when')
        grouped = self.group_functions(filtered)

        context.update({
            'calls': grouped,
            'calls_json': json.dumps(grouped),
        })
        return context


class ListView(LoginRequiredMixin, TemplateView):
    template_name = "api_calls/list.html"

    def filter_code(self, context, data):
        context['active_code'] = 'All'
        if not 'code' in self.request.GET:
            return data

        code = self.request.GET['code'].lower()
        if not code or code.lower() == 'all':
            return data

        filtered = [x for x in data if x['code'] == code]
        if filtered:
            context['active_code'] = code
        return filtered

    def scrub(self, data):
        for call in data:
            # to make it work for humanize
            call['when'] = datetime.strptime(call['when'], '%Y-%m-%d %H:%M:%S')
        return data

    def get_context_data(self, **kwargs):
        context = super(ListView, self).get_context_data(**kwargs)
        filtered = deepcopy(CALLS)

        codes = list(set([x['code'] for x in CALLS]))
        codes.sort()

        filtered = self.filter_code(context, filtered)
        filtered = filter_time(self.request, context, filtered, 'when')
        filtered = self.scrub(filtered)

        context.update({
            'codes': codes,
            'calls': filtered,
        })
        return context
