
from django.shortcuts import render

# Create your views here.
# -*- coding: utf-8 -*-
"""
Views of Accounts app
"""
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
import json
from django.urls import reverse_lazy
from django.views.generic import FormView
from obp.api import API, APIError
from .forms import CreateAccountForm
from django.utils.translation import ugettext_lazy as _

class IndexAccountsView(LoginRequiredMixin, FormView):

    """Index view for Accounts"""
    template_name = "accounts/index.html"
    form_class = CreateAccountForm
    success_url = reverse_lazy('accounts-create')

    def dispatch(self, request, *args, **kwargs):
        self.api = API(request.session.get('obp'))
        return super(IndexAccountsView, self).dispatch(request, *args, **kwargs)

    def get_form(self, *args, **kwargs):
        form = super(IndexAccountsView, self).get_form(*args, **kwargs)
        # Cannot add api in constructor: super complains about unknown kwarg
        form.api = self.api
        fields = form.fields
        try:
            fields['bank_id'].choices = self.api.get_bank_id_choices()
        except APIError as err:
            messages.error(self.request, err)
        except Exception as err:
            messages.error(self.request, err)
        return form

    def form_valid(self, form):
        try:
            data = form.cleaned_data
            #urlpath = '/banks/{}/accounts/{}'.format(data['bank_id'], data['account_id'])
            urlpath = '/banks/{}/accounts'.format(data['bank_id'])
            payload ={
                "user_id": data["user_id"],
                "label": data["label"],
                "product_code": data["product_code"],
                "branch_id": data["branch_id"],
                "balance": {
                    "currency": data["balance_currency"] if data["balance_currency"] is not None else "EUR",
                    "amount": data["balance_amount"] if data["balance_amount"] is not None else 0
                },
                "account_routings": [{
                    "scheme": data["account_routings_scheme"] if data["account_routings_scheme"] !="" else "scheme",
                    "address": data["account_routings_address"] if data["account_routings_address"]!="" else "address"
                }],
            }
            result = self.api.post(urlpath, payload=payload)
        except APIError as err:
            messages.error(self.request, "Unknown Error")
            return super(IndexAccountsView, self).form_invalid(form)
        except Exception as err:
            messages.error(self.request, err, "Unknown Error")
            return super(IndexAccountsView, self).form_invalid(form)
        if 'code' in result and result['code']>=400:
            messages.error(self.request, result['message'])
            return super(IndexAccountsView, self).form_valid(form)
        msg = 'Account has been created successfully!'
        messages.success(self.request, msg)
        return super(IndexAccountsView, self).form_valid(form)
