# -*- coding: utf-8 -*-
"""
Views of users app
"""
import datetime
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse, reverse_lazy
from django.views.generic import FormView, TemplateView, View

from base.filters import BaseFilter
from obp.api import API, APIError
from .forms import AddEntitlementForm,CreateInvitationForm
import csv

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
            if 'code' in entitlements and entitlements['code'] >= 400:
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
        users = []
        context = super(IndexView, self).get_context_data(**kwargs)

        api = API(self.request.session.get('obp'))
        limit = self.request.GET.get('limit', 50)
        offset = self.request.GET.get('offset', 0)
        email = self.request.GET.get('email')
        username = self.request.GET.get('username')
        lockedstatus = self.request.GET.get('locked_status')
        if lockedstatus is None: lockedstatus = "active"

        if email:
            urlpath = '/users/email/{}/terminator'.format(email)
        elif username:
            urlpath = '/users/username/{}'.format(username)
        else:
            urlpath = '/users?limit={}&offset={}&locked_status={}'.format(limit, offset, lockedstatus)

        try:
            response = api.get(urlpath)
            if 'code' in response and response['code'] >= 400:
                messages.error(self.request, response['message'])
            else:
                users = response
        except APIError as err:
            messages.error(self.request, err)
        except Exception as err:
            messages.error(self.request, err)

        role_names = self.get_users_rolenames(context)
        try:
            users = FilterRoleName(context, self.request.GET) \
                .apply([users] if username else users['users'])
        except Exception as err:
            messages.error(self.request, err)
            users = []
        context.update({
            'role_names': role_names,
            'statistics': {
                'users_num': len(users),
            },
            'users': users,
            'limit': limit,
            'offset': offset,
            'locked_status': lockedstatus
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
        except Exception as err:
            messages.error(self.request, err)
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
        except Exception as err:
            messages.error(self.request, err)
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
        except Exception as err:
            messages.error(self.request, err)

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
        except Exception as err:
            messages.error(self.request, err)
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
            messages.error(self.request, err)
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
            messages.error(self.request, err)
        user["entitlements"]["list"] = sorted(user["entitlements"]["list"], key=lambda d: d['role_name'])
        context.update({
            'apiuser': user,  # 'user' is logged-in user in template context
        })
        return context


class InvitationView(LoginRequiredMixin, FormView):
    """View to create a User Invitation"""
    form_class = CreateInvitationForm
    template_name = 'users/invitation.html'
    success_url = reverse_lazy('my-user-invitation')

    def dispatch(self, request, *args, **kwargs):
        self.api = API(request.session.get('obp'))
        return super(InvitationView, self).dispatch(request, *args, **kwargs)

    def get_form(self, *args, **kwargs):
        form = super(InvitationView, self).get_form(*args, **kwargs)
        form.api = self.api
        fields = form.fields
        try:
            fields['bank_id'].choices = self.api.get_bank_id_choices()
        except APIError as err:
            messages.error(self.request, err)
        except Exception as err:
            messages.error(self.request, err)
        return form

    def form_valid(self, form, **kwargs):
        data = form.cleaned_data
        post_url_path = '/banks/{}/user-invitation'.format(data['bank_id'])
        get_url_path = '/banks/{}/user-invitations'.format(data['bank_id'])
        invitations=[]
        payload = {
            'first_name': data['first_name'],
            'last_name': data['last_name'],
            'email': data['email'],
            'company': data['company'],
            'country': data['country'],
            'purpose': 'DEVELOPER'
        }
        context = self.get_context_data(**kwargs)
        try:
            result = self.api.post(post_url_path, payload=payload)
            if 'code' in result and result['code'] >= 400:
                messages.error(self.request, result['message'])
                return super(InvitationView, self).form_valid(form)
            else:
                self.get_invitations(context, get_url_path, invitations)
                msg = 'User Invitation ({}) at Bank({}) has been {}!'.format(result['first_name'],data['bank_id'], result['status'] )
                messages.success(self.request, msg)
                return self.render_to_response(context)
        except APIError as err:
            messages.error(self.request, err)
            return super(InvitationView, self).form_invalid(form)
        except Exception as err:
            messages.error(self.request, err)
            return super(InvitationView, self).form_invalid(form)

    def get_invitations(self, context, get_url_path, invitations):
        response = self.api.get(get_url_path)
        if 'code' in response and response['code'] >= 400:
            messages.error(self.request, response['message'])
        else:
            invitations = invitations + response['user_invitations']
        context.update({
            'invitations': invitations,
        })


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
        except Exception as err:
            messages.error(self.request, err)

        # from sonarcloud: Change this code to not perform redirects based on user-controlled data.    
        redirect_url_from_gui = request.POST.get('next', reverse('users-index'))
        if "/users/all/user_id/" in str(redirect_url_from_gui):
            redirect_url = reverse('users-detail',kwargs={"user_id":kwargs['user_id']})
        elif ("/users/myuser/user_id/" in str(redirect_url_from_gui)):
            redirect_url = reverse('my-user-detail',kwargs={"user_id":kwargs['user_id']})
        else:
             redirect_url = reverse('users-index')
        
        return HttpResponseRedirect(redirect_url)


class UserStatusUpdateView(LoginRequiredMixin, View):
    """View to delete a user"""

    def post(self, request, *args, **kwargs):
        """Deletes a user via API"""
        api = API(self.request.session.get('obp'))
        try:
            if(request.POST.get("Delete")):
                self._delete_user(api, request, args, kwargs)
            elif(request.POST.get("Lock")):
                self._lock_user(api, request, args, kwargs)
            else:
                self._lock_status_user(api, request, args, kwargs)

        except APIError as err:
            messages.error(request, err)
        except Exception as err:
            messages.error(self.request, err)

        # from sonarcloud: Change this code to not perform redirects based on user-controlled data.
        redirect_url_from_gui = request.POST.get('next', reverse('users-index'))
        if "/users/all/user_id/" in str(redirect_url_from_gui):
            redirect_url = reverse('users-detail', kwargs={"user_id": kwargs['user_id']})
        elif ("/users/myuser/user_id/" in str(redirect_url_from_gui)):
            redirect_url = reverse('my-user-detail', kwargs={"user_id": kwargs['user_id']})
        else:
            redirect_url = reverse('users-index')

        return HttpResponseRedirect(redirect_url)

    def _delete_user(self, api, request, *args, **kwargs):
        urlpath = '/users/{}'.format(kwargs['user_id'])
        result = api.delete(urlpath)
        if result is not None and 'code' in result and result['code'] >= 400:
            messages.error(request, result['message'])
        else:
            msg = 'User with ID {} has been deleted.'.format(kwargs['user_id'])
            messages.success(request, msg)

    def _lock_user(self, api, request, *args, **kwargs):
        urlpath = '/users/{}/locks'.format(kwargs['username'])
        result = api.post(urlpath, None)
        if result is not None and 'code' in result and result['code'] >= 400:
            messages.error(request, result['message'])
        else:
            msg = 'User {} has been lock.'.format(kwargs['username'])
            messages.success(request, msg)

    def _lock_status_user(self, api, request, *args, **kwargs):
        urlpath = '/users/{}/lock-status'.format(kwargs['username'])
        result = api.put(urlpath, None)
        #if result is not None and 'code' in result and result['code'] >= 400:
        if 'code' in result and result['code'] == 404:
            msg = 'User {} has been unlocked.'.format(kwargs['username'])
            messages.success(request, msg)
        else:
            messages.error(request, result['message'])
        #else:
        #    msg = 'User {} has been unlocked.'.format(kwargs['username'])
        #    messages.success(request, msg)

class ExportCsvView(LoginRequiredMixin, View):
    """View to export the user to csv"""
    def get(self, request, *args, **kwargs):
        users = []
        api = API(self.request.session.get('obp'))
        limit = self.request.GET.get('limit', 50)
        offset = self.request.GET.get('offset', 0)
        email = self.request.GET.get('email')
        username = self.request.GET.get('username')
        lockedstatus = self.request.GET.get('locked_status')
        if lockedstatus is None: lockedstatus = "active"
        if email:
            urlpath = '/users/email/{}/terminator'.format(email)
        elif username:
            urlpath = '/users/username/{}'.format(username)
        else:
            urlpath = '/users?limit={}&offset={}&locked_status={}'.format(limit, offset, lockedstatus)
        try:
            response = api.get(urlpath)
            if 'code' in response and response['code'] >= 400:
                messages.error(self.request, response['message'])
            else:
                users = response['users']

        except APIError as err:
            messages.error(self.request, err)
        except Exception as err:
            messages.error(self.request, err)
        response = HttpResponse(content_type = 'text/csv')
        response['Content-Disposition'] = 'attachment;filename= Users'+ str(datetime.datetime.now())+'.csv'
        writer = csv.writer(response)
        writer.writerow(["username","user_id","email","provider_id","provider","last_marketing_agreement_signed_date"])
        for user in users:
            writer.writerow([user['username'], user['user_id'], user['email'], user['provider_id'], user['provider'],
                             user['last_marketing_agreement_signed_date']])
        return response

