# -*- coding: utf-8 -*-
"""
Views of users app
"""

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import TemplateView, View

from base.filters import BaseFilter
from base.api import api, APIError


class FilterRoleName(BaseFilter):
    """Filter users by role names"""
    filter_type = 'role_name'

    def _apply(self, data, filter_value):
        filtered = [x for x in data if filter_value in [
            e['role_name'] for e in x['entitlements']['list']
        ]]
        return filtered



class IndexView(LoginRequiredMixin, TemplateView):
    """Index view for users"""
    template_name = "users/index.html"

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        role_names = []
        users = []
        try:
            urlpath = '/users'
            users = api.get(self.request, urlpath)
            for user in users['users']:
                for entitlement in user['entitlements']['list']:
                    role_names.append(entitlement['role_name'])
            role_names = list(set(role_names))
            role_names.sort()
            users = FilterRoleName(context, self.request.GET)\
                .apply(users['users'])
        except APIError as err:
            messages.error(self.request, err)

        context.update({
            'role_names': role_names,
            'statistics': {
                'users_num': len(users),
            },
            'users': users,
        })
        return context



class DetailView(LoginRequiredMixin, TemplateView):
    """Detail view for a user"""
    template_name = 'users/detail.html'

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)

        # NOTE: assuming there is just one user with that email address
        # The API actually needs a 'get user by id'
        user = {}
        try:
            urlpath = '/users/{}'.format(kwargs['user_email'])
            users = api.get(self.request, urlpath)
            if len(users['users']) > 0:
                user = users['users'][0]
                try:
                    urlpath = '/users/{}/entitlements'.format(user['user_id'])
                    entitlements = api.get(self.request, urlpath)
                    user['entitlements'] = entitlements['list']
                except APIError as err:
                    messages.error(self.request, err)
        except APIError as err:
            messages.error(self.request, err)

        context.update({
            'apiuser': user,
        })
        return context



class AddEntitlementView(LoginRequiredMixin, View):
    """View to add an entitlement by role name (and bank ID)"""

    def post(self, request, *args, **kwargs):
        """Posts entitlement data to API"""
        try:
            urlpath = '/users/{}/entitlements'.format(kwargs['user_id'])
            payload = {
                'bank_id': request.POST['bank_id'],
                'role_name': request.POST['role_name'],
            }
            entitlement = api.post(request, urlpath, payload=payload)
            msg = 'Entitlement with role {} has been added.'.format(
                entitlement['role_name'])
            messages.success(request, msg)
        except APIError as err:
            messages.error(request, err)

        redirect_url = reverse('users-detail', kwargs={
            'user_email': request.POST['user_email'],
        })
        return HttpResponseRedirect(redirect_url)



class DeleteEntitlementView(LoginRequiredMixin, View):
    """View to delete an entitlement"""

    def post(self, request, *args, **kwargs):
        """Deletes entitlement from API"""
        try:
            urlpath = '/users/{}/entitlement/{}'.format(
                kwargs['user_id'], kwargs['entitlement_id'])
            api.delete(request, urlpath)
            msg = 'Entitlement with role {} has been deleted.'.format(
                request.POST['role_name'])
            messages.success(request, msg)
        except APIError as err:
            messages.error(request, err)

        redirect_url = reverse('users-detail', kwargs={
            'user_email': request.POST['user_email'],
        })
        return HttpResponseRedirect(redirect_url)
