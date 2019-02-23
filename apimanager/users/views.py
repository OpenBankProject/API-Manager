# -*- coding: utf-8 -*-
"""
Views of users app
"""

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import FormView, TemplateView, View

from base.filters import BaseFilter
from obp.api import API, APIError

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


class FilterUsername(BaseFilter):
    """Filter users by username """
    filter_type = 'username'

    def _apply(self, data, filter_value):
        filtered = [x for x in data if x['username'].find(filter_value) != -1]
        return filtered


class IndexView(LoginRequiredMixin, TemplateView):
    """Index view for users"""
    template_name = "users/index.html"

    def get_users_rolenames(self, context):

        api = API(self.request.session.get('obp'))

        role_names = []
        try:
            urlpath = '/entitlements'
            entitlements = api.get(urlpath)
            if 'code' in entitlements and entitlements['code']>=400:
                messages.error(self.request, entitlements['message'])
            else:
                for entitlement in entitlements['list']:
                    role_names.append(entitlement['role_name'])
        except APIError as err:
            messages.error(self.request, err)
            return [], []
        # fail gracefully in case API provides new structure
        except KeyError as err:
            messages.error(self.request, 'KeyError: {}'.format(err))
            return [], []

        role_names = list(set(role_names))
        role_names.sort()

        return role_names

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)

        api = API(self.request.session.get('obp'))
        limit = self.request.GET.get('limit', 50)
        offset = self.request.GET.get('offset', 0)
        email = self.request.GET.get('email')
        username = self.request.GET.get('username')

        if email:
            urlpath = '/users/email/{}/terminator'.format(email)
        elif username:
            urlpath = '/users/username/{}'.format(username)
        else:
            urlpath = '/users?limit={}&offset={}'.format(limit, offset)

        users = []
        try:
            users = api.get(urlpath)
        except APIError as err:
            messages.error(self.request, err)
        except:
            messages.error(self.request, 'Unknown Error')

        role_names = self.get_users_rolenames(context)
        try:
            users = FilterRoleName(context, self.request.GET) \
                .apply([users] if username else users['users'])
        except:
            users = []
        context.update({
            'role_names': role_names,
            'statistics': {
                'users_num': len(users),
            },
            'users': users,
            'limit': limit,
            'offset': offset
        })
        return context


class DetailView(LoginRequiredMixin, FormView):
    """Detail view for a user"""
    form_class = AddEntitlementForm
    template_name = 'users/detail.html'

    def dispatch(self, request, *args, **kwargs):
        self.api = API(request.session.get('obp'))
        return super(DetailView, self).dispatch(request, *args, **kwargs)

    def get_form(self, *args, **kwargs):
        form = super(DetailView, self).get_form(*args, **kwargs)
        try:
            form.fields['bank_id'].choices = self.api.get_bank_id_choices()
        except APIError as err:
            messages.error(self.request, err)
        except:
            messages.error(self.request, 'Unknown Error')
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
            entitlement = self.api.post(urlpath, payload=payload)
        except APIError as err:
            messages.error(self.request, err)
            return super(DetailView, self).form_invalid(form)
        except:
            messages.error(self.request, 'Unknown Error')
            return super(DetailView, self).form_invalid(form)
        if 'code' in entitlement and entitlement['code']>=400:
            messages.error(self.request, entitlement['message'])
            return super(DetailView, self).form_invalid(form)
        else:
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
            urlpath = '/users/user_id/{}'.format(self.kwargs['user_id'])
            user = self.api.get(urlpath)
            if 'code' in user and user['code']>=400:
                messages.error(self.request, user['message'])
            else:
                context['form'].fields['user_id'].initial = user['user_id']
        except APIError as err:
            messages.error(self.request, err)
        except:
            messages.error(self.request, 'Unknown Error')

        context.update({
            'apiuser': user,  # 'user' is logged-in user in template context
        })
        return context


class MyDetailView(LoginRequiredMixin, FormView):
    """Detail view for a current user"""
    form_class = AddEntitlementForm
    template_name = 'users/detail.html'

    def dispatch(self, request, *args, **kwargs):
        self.api = API(request.session.get('obp'))
        return super(MyDetailView, self).dispatch(request, *args, **kwargs)

    def get_form(self, *args, **kwargs):
        form = super(MyDetailView, self).get_form(*args, **kwargs)
        try:
            form.fields['bank_id'].choices = self.api.get_bank_id_choices()
        except APIError as err:
            messages.error(self.request, err)
        except:
            messages.error(self.request, 'Unknown Error')
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
            entitlement = self.api.post(urlpath, payload=payload)
            if 'code' in entitlement and entitlement['code'] >= 400:
                messages.error(self.request, entitlement['message'])
            else:
                msg = 'Entitlement with role {} has been added.'.format(entitlement['role_name'])
                messages.success(self.request, msg)
            self.success_url = self.request.path
        except APIError as err:
            messages.error(self.request, err)
            return super(MyDetailView, self).form_invalid(form)
        except Exception as err:
            messages.error(self.request, 'Unknown Error. {}'.format(err))
            return super(MyDetailView, self).form_invalid(form)
        else:
            return super(MyDetailView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(MyDetailView, self).get_context_data(**kwargs)
        # NOTE: assuming there is just one user with that email address
        # The API needs a call 'get user by id'!
        user = {}
        try:
            urlpath = '/users/current'
            user = self.api.get(urlpath)
            context['form'].fields['user_id'].initial = user['user_id']
        except APIError as err:
            messages.error(self.request, err)
        except Exception as err:
            messages.error(self.request, 'Unknown Error')

        context.update({
            'apiuser': user,  # 'user' is logged-in user in template context
        })
        return context


class DeleteEntitlementView(LoginRequiredMixin, View):
    """View to delete an entitlement"""

    def post(self, request, *args, **kwargs):
        """Deletes entitlement from API"""
        api = API(self.request.session.get('obp'))
        try:
            urlpath = '/users/{}/entitlement/{}'.format(
                kwargs['user_id'], kwargs['entitlement_id'])
            result = api.delete(urlpath)
            if result is not None and 'code' in result and result['code']>=400:
                messages.error(request, result['message'])
            else:
                msg = 'Entitlement with role {} has been deleted.'.format(
                    request.POST.get('role_name', '<undefined>'))
                messages.success(request, msg)
        except APIError as err:
            messages.error(request, err)
        except:
            messages.error(self.request, 'Unknown Error')

        redirect_url = request.POST.get('next', reverse('users-index'))
        return HttpResponseRedirect(redirect_url)
