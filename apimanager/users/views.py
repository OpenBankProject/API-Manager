# -*- coding: utf-8 -*-
"""
Views of users app
"""

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic import FormView, TemplateView, View

from base.filters import BaseFilter
from base.api import api, APIError
from base.api_helper import get_bank_id_choices

from .forms import AddEntitlementForm


class FilterRoleName(BaseFilter):
    """Filter users by role names"""
    filter_type = 'role_name'

    def _apply(self, data, filter_value):
        filtered = [x for x in data if filter_value in [
            e['role_name'] for e in x['entitlements']['list']
        ]]
        return filtered


class FilterEmail(BaseFilter):
    """Filter users by email address"""
    filter_type = 'email'

    def _apply(self, data, filter_value):
        filtered = [x for x in data if x['email'].find(filter_value) != -1]
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
            users = FilterEmail(context, self.request.GET)\
                .apply(users)
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


class DetailView(LoginRequiredMixin, FormView):
    """Detail view for a user"""
    form_class = AddEntitlementForm
    template_name = 'users/detail.html'

    def get_form(self, *args, **kwargs):
        form = super(DetailView, self).get_form(*args, **kwargs)
        form.fields['bank_id'].choices = get_bank_id_choices(self.request)
        return form

    def form_valid(self, form):
        """Posts entitlement data to API"""
        try:
            data = form.cleaned_data
            urlpath = '/users/{}/entitlements'.format(data['user_id'])
            payload = {
                'bank_id': data['bank_id'],
                'role_name': data['role_name'],
            }
            entitlement = api.post(self.request, urlpath, payload=payload)
        except APIError as err:
            messages.error(self.request, err)
            return super(DetailView, self).form_invalid(form)

        msg = 'Entitlement with role {} has been added.'.format(
            entitlement['role_name'])
        messages.success(self.request, msg)
        self.success_url = self.request.path
        return super(DetailView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)

        # NOTE: assuming there is just one user with that email address
        # The API needs a call 'get user by id'!
        user = {}
        try:
            urlpath = '/users/{}'.format(self.kwargs['user_email'])
            users = api.get(self.request, urlpath)
            if len(users['users']) > 0:
                user = users['users'][0]
                context['form'].fields['user_id'].initial = user['user_id']
        except APIError as err:
            messages.error(self.request, err)

        context.update({
            'apiuser': user,  # 'user' is logged-in user in template context
        })
        return context


class DeleteEntitlementView(LoginRequiredMixin, View):
    """View to delete an entitlement"""

    def post(self, request, *args, **kwargs):
        """Deletes entitlement from API"""
        try:
            urlpath = '/users/{}/entitlement/{}'.format(
                kwargs['user_id'], kwargs['entitlement_id'])
            api.delete(request, urlpath)
            msg = 'Entitlement with role {} has been deleted.'.format(
                request.POST.get('role_name', '<undefined>'))
            messages.success(request, msg)
        except APIError as err:
            messages.error(request, err)

        redirect_url = request.POST.get('next', reverse('users-index'))
        return HttpResponseRedirect(redirect_url)
