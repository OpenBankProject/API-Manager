# -*- coding: utf-8 -*-

import json
from copy import deepcopy
from datetime import datetime

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import TemplateView, RedirectView, View

from base.filters import BaseFilter
from base.utils import api_get, api_post, api_delete


class FilterRoleName(BaseFilter):
    filter_type = 'role_name'

    def _apply(self, data, filter_value):
        filtered = [x for x in data if filter_value in [e['role_name'] for e in x['entitlements']['list']]]
        return filtered



class IndexView(LoginRequiredMixin, TemplateView):
    template_name = "users/index.html"

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        role_names = []
        filtered = []
        urlpath = '/users'
        users = api_get(self.request, urlpath)

        if not isinstance(users, dict):
            messages.error(self.request, users)
        elif 'error' in users:
            messages.error(self.request, users['error'])
        else:
            for user in users['users']:
                for entitlement in user['entitlements']['list']:
                    role_names.append(entitlement['role_name'])
            role_names = list(set(role_names))
            role_names.sort()
            filtered = FilterRoleName(context, self.request.GET)\
                .apply(users['users'])


        context.update({
            'role_names': role_names,
            'statistics': {
                'users_num': len(filtered),
            },
            'users': filtered,
        })
        return context



class DetailView(LoginRequiredMixin, TemplateView):
    template_name = 'users/detail.html'

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        # NOTE: assuming there is just one user with that email address
        # The API actually needs a 'get user by id'
        urlpath = '/users/{}'.format(kwargs['user_email'])
        users = api_get(self.request, urlpath)
        user = {}
        if 'error' in users:
            messages.error(self.request, users['error'])
        elif len(users['users']) > 0:
            user = users['users'][0]
            urlpath = '/users/{}/entitlements'.format(user['user_id'])
            entitlements = api_get(self.request, urlpath)
            if 'error' in entitlements:
                messages.error(self.request, entitlements['error'])
            else:
                user['entitlements'] = entitlements['list']
        context.update({
            'user': user,
        })
        return context



class AddEntitlementView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        urlpath = '/users/{}/entitlements'.format(kwargs['user_id'])
        payload = {
            'bank_id': request.POST['bank_id'],
            'role_name': request.POST['role_name'],
        }
        entitlement = api_post(request, urlpath, payload=payload)
        if not isinstance(entitlement, dict):
            messages.error(request, entitlement)
        elif 'error' in entitlement:
            messages.error(request, entitlement['error'])
        else:
            msg = 'Entitlement with role {} has been added.'.format(
                entitlement['role_name'])
            messages.success(request, msg)
        redirect_url = reverse('users-detail', kwargs={
            'user_email': request.POST['user_email'],
        })
        return HttpResponseRedirect(redirect_url)



class DeleteEntitlementView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        urlpath = '/users/{}/entitlement/{}'.format(
            kwargs['user_id'], kwargs['entitlement_id'])
        result = api_delete(request, urlpath)
        if 'error' in result:
            messages.error(request, result['error'])
        else:
            msg = 'Entitlement with role {} has been deleted.'.format(
                request.POST['role_name'])
            messages.success(request, msg)
        redirect_url = reverse('users-detail', kwargs={
            'user_email': request.POST['user_email'],
        })
        return HttpResponseRedirect(redirect_url)
