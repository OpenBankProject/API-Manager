
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
from apimanager.settings import DEBUG

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
            urlpath = '/banks'
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

class UpdateBanksView(LoginRequiredMixin, FormView):
    template_name = "banks/update.html"
    form_class = CreateBankForm
    success_url = '/banks/list'

    def dispatch(self, request, *args, **kwargs):
        self.api = API(request.session.get('obp'))
        return super(UpdateBanksView, self).dispatch(request, *args, **kwargs)

    def get_form(self, *args, **kwargs):
        form = super(UpdateBanksView, self).get_form(*args, **kwargs)
        # Cannot add api in constructor: super complains about unknown kwarg
        form.api = self.api
        fields = form.fields

        try:
            fields['bank_id'].choices = self.api.get_bank_id_choices()
        except APIError as err:
            messages.error(self.request, err)
        except Exception as err:
            messages.error(self.request, err)
        try:

           urlpath = '/banks/{}'.format(self.kwargs["bank_id"])
           result = self.api.get(urlpath)
           fields['bank_id'].initial = self.kwargs['bank_id']
           fields['bank_code'].initial = result['bank_code']
           fields['full_name'].initial = result['full_name']
           fields['logo'].initial = result['logo']
           fields['website'].initial = result['website']
           fields['bank_routings_scheme'].initial = result['bank_routings'][0]["scheme"]
           fields['bank_routings_address'].initial = result['bank_routings'][0]["address"]
        except Exception as err:
            if DEBUG:
                raise(err)
            messages.error(self.request, "Unknown Error {}".format(err))
        return form


    #Check form validation, when update previous ATM
    def form_valid(self, form):
        data = form.cleaned_data
        print("data is:", data)
        urlpath = '/banks'
        payload ={
            "id": data["bank_id"],
            "bank_code": data["bank_code"],
            "full_name":data["full_name"],
            "logo":data["logo"],
            "website":data["website"],
            "bank_routings_scheme": data["bank_routings_scheme"] if data["bank_routings_scheme"] is not None else "",
            "bank_routings_address": data["bank_routings_address"] if data["bank_routings_address"] is not None else ""
        }
        try:
            result = self.api.put(urlpath, payload=payload)
            print("result is:", result)
            if 'code' in result and result['code']>=400:
                messages.error(self.request, result['message'])
                return super(UpdateBanksView, self).form_invalid(form)
        except APIError as err:
            if DEBUG:
                raise(err)
            messages.error(self.request, err)
            return super(UpdateBanksView, self).form_invalid(form)
        except Exception as e:
            if DEBUG:
                raise(err)
            messages.error(self.request, e)
            return super(UpdateBanksView, self).form_invalid(form)
        msg = 'Bank {} has been updated successfully!'.format(  # noqa
            data["bank_id"])
        messages.success(self.request, msg)
        return super(UpdateBanksView, self).form_valid(form)
