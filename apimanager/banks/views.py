
from django.shortcuts import render

# Create your views here.
# -*- coding: utf-8 -*-
"""
Views of banks app
"""
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
import json
from django.urls import reverse_lazy
from django.views.generic import FormView
from obp.api import API, APIError
from .forms import CreateBankForm
from django.utils.translation import ugettext_lazy as _

class IndexBanksView(LoginRequiredMixin, FormView):

    """Index view for Banks"""
    template_name = "banks/index.html"
    form_class = CreateBankForm
    success_url = reverse_lazy('banks_create')

    def dispatch(self, request, *args, **kwargs):
        self.api = API(request.session.get('obp'))
        return super(IndexBanksView, self).dispatch(request, *args, **kwargs)

    def get_form(self, *args, **kwargs):
        form = super(IndexBanksView, self).get_form(*args, **kwargs)
        # Cannot add api in constructor: super complains about unknown kwarg
        form.api = self.api
        fields = form.fields
        try:
            pass
        except APIError as err:
            messages.error(self.request, err)
        except Exception as err:
            messages.error(self.request, err)

        return form

    # Form Valid, when create a new Bank
    def form_valid(self, form):
        try:
            data = form.cleaned_data
            urlpath = 'v5.1.0/banks'
            payload ={
                "id": data["bank_id"],
                "bank_code": data["bank_code"],
                "full_name":data["full_name"],
                "logo":data["logo"],
                "website":data["website"],
                **self._routing(data)
            }
            result = self.api.post(urlpath, payload=payload)
        except APIError as err:
            messages.error(self.request, err)
            return super(IndexBanksView, self).form_invalid(form)
        except Exception as err:
            messages.error(self.request, err)
            return super(IndexBanksView, self).form_invalid(form)
        if 'code' in result and result['code']>=400:
            messages.error(self.request, result['message'])
            return super(IndexBanksView, self).form_valid(form)
        msg = 'Bank {} has been created successfully!'.format(result['id'])
        messages.success(self.request, msg)
        return super(IndexBanksView, self).form_valid(form)

    def _routing(self, data):
        return  {
            "bank_routings_scheme": data["bank_routings_scheme"] if data["bank_routings_scheme"] is not None else "",
            "bank_routings_address": data["bank_routings_address"] if data["bank_routings_address"] is not None else ""
        }

