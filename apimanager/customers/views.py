# -*- coding: utf-8 -*-
"""
Views of customers app
"""

import datetime

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import FormView

from base.api import api, APIError

from .forms import CreateCustomerForm, DATETIME_INPUT_FORMAT


class CreateView(LoginRequiredMixin, FormView):
    """View to create a customer"""
    form_class = CreateCustomerForm
    template_name = 'customers/create.html'
    success_url = reverse_lazy('customers-create')

    def get_bank_id_choices(self):
        choices = [('', 'Choose ...')]
        try:
            result = api.get(self.request, '/banks')
            for bank in result['banks']:
                choices.append((bank['id'], bank['short_name']))
        except APIError as err:
            messages.error(err)
        return choices

    def get_user_id_choices(self):
        choices = [('', 'Choose ...')]
        try:
            result = api.get(self.request, '/users')
            for user in result['users']:
                choices.append((user['user_id'], user['username']))
        except APIError as err:
            messages.error(err)
        return choices

    def get_form(self, *args, **kwargs):
        form = super(CreateView, self).get_form(*args, **kwargs)
        fields = form.fields
        fields['bank_id'].choices = self.get_bank_id_choices()
        fields['user_id'].choices = self.get_user_id_choices()
        fields['last_ok_date'].initial =\
            datetime.datetime.now().strftime(DATETIME_INPUT_FORMAT)
        return form

    def form_valid(self, form):
        try:
            data = form.cleaned_data
            urlpath = '/banks/{}/customers'.format(data['bank_id'])
            if data['dob_of_dependants']:
                dob_of_dependants = data['dob_of_dependants'].split(',')
            else:
                dob_of_dependants = []
            payload = {
                'user_id': data['user_id'],
                'customer_number': data['customer_number'],
                'legal_name': data['legal_name'],
                'mobile_phone_number': data['mobile_phone_number'],
                'email': data['email'],
                'face_image': {
                    'url': data['face_image_url'],
                    'date':
                        data['face_image_date'].strftime(DATETIME_INPUT_FORMAT),
                },
                'date_of_birth':
                    data['date_of_birth'].strftime(DATETIME_INPUT_FORMAT),
                'relationship_status': data['relationship_status'],
                'dependants': data['dependants'],
                'dob_of_dependants': dob_of_dependants,
                'credit_rating': {
                    'rating': data['credit_rating_rating'],
                    'source': data['credit_rating_source'],
                },
                'credit_limit': {
                    'currency': data['credit_limit_currency'],
                    'amount': data['credit_limit_amount'],
                },
                'highest_education_attained':
                    data['highest_education_attained'],
                'employment_status': data['employment_status'],
                'kyc_status': data['kyc_status'],
                'last_ok_date':
                    data['last_ok_date'].strftime(DATETIME_INPUT_FORMAT),
            }
            result = api.post(self.request, urlpath, payload=payload)
        except APIError as err:
            messages.error(self.request, err)
            return super(CreateView, self).form_invalid(form)

        msg = 'Customer number {} has been created successfully!'.format(
            result['customer_number'])
        messages.success(self.request, msg)
        return super(CreateView, self).form_valid(form)
