# -*- coding: utf-8 -*-

import json
from copy import deepcopy
from datetime import datetime

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from base.filters import filter_time
from base.utils import json_serial, api_get


APIUSER = [
    {
        'id': 1,
        'email': 'sebastian@tesobe.com',
        'name_': 'Sebastian Henschel',
        'userid_': 'zyzop',
        #'userid_': '05c98d97-5d6d-46b5-a880-2da0a45019c8',
        'last_login': '2016-09-07 12:34:47',
        'whatever': 'dfasdfsd',
    },
    {
        'id': 2,
        'email': 'robert.x.0.gh@example.com',
        'name_': 'Robert X.0.GH',
        'userid_': 'ff3f94f9-bbd6-4cd9-ab78-3701e961eb58',
        'last_login': '2016-08-10 16:34:47',
        'whatever': 'ijkjkljljk',
    },
]


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = "users/index.html"

    def filter_role_name(self, context, data):
        context['active_role_name'] = 'All'
        if not 'role_name' in self.request.GET:
            return data
        role_name = self.request.GET['role_name']
        if not role_name or role_name.lower() == 'all':
            return data

        filtered = []
        for user in data:
            for entitlement in user['entitlements']:
                if role_name == entitlement['role_name']:
                    filtered.append(user)
                    break

        if filtered:
            context['active_role_name'] = role_name
        return filtered

    def scrub(self, data):
        for user in data:
            user['last_login'] = datetime.strptime(user['last_login'], '%Y-%m-%d %H:%M:%S')
        return data

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        filtered = deepcopy(APIUSER)
        role_names = []

        for user in filtered:
            urlpath = '/users/{}/entitlements'.format(user['userid_'])
            entitlements = api_get(self.request, urlpath)
            if 'error' in entitlements:
                messages.error(self.request, entitlements['error'])
                break
            else:
                user['entitlements'] = []
                for entitlement in entitlements['list']:
                    user['entitlements'].append(entitlement)
                    if entitlement['role_name'] == 'SuperAdmin':
                        user['is_super_admin'] = True
                    role_names.append(entitlement['role_name'])
        role_names = list(set(role_names))
        role_names.sort()

        filtered = self.filter_role_name(context, filtered)
        filtered = filter_time(self.request, context, filtered, 'last_login')
        filtered = self.scrub(filtered)

        context.update({
            'role_names': role_names,
            'users': filtered,
            'users_json': json.dumps(filtered, default=json_serial),
        })
        return context
