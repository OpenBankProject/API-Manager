from django.shortcuts import render

# Create your views here.
# -*- coding: utf-8 -*-
"""
Views of Product app
"""

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
import json
from django.urls import reverse_lazy
from django.views.generic import FormView
from obp.api import API, APIError
from .forms import CreateProductForm
from django.views.decorators.csrf import csrf_exempt
from base.utils import exception_handle

class IndexProductView(LoginRequiredMixin, FormView):
    """Index view for Product"""
    template_name = "products/index.html"
    form_class = CreateProductForm
    success_url = reverse_lazy('products-create')

    def dispatch(self, request, *args, **kwargs):
        self.api = API(request.session.get('obp'))
        return super(IndexProductView, self).dispatch(request, *args, **kwargs)

    def get_form(self, *args, **kwargs):
        form = super(IndexProductView, self).get_form(*args, **kwargs)
        # Cannot add api in constructor: super complains about unknown kwarg
        form.api = self.api
        fields = form.fields
        print(fields, "These are fields")
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
           print(data, "This is a data")
           urlpath = '/banks/{}/products'.format(bank_id)
           payload={
                "parent_product_code": data["parent_product_code"],
                "name": data["name"],
                "more_info_url": data["more_info_url"],
                "terms_and_conditions_url": data["terms_and_conditions_url"],
                "description": data["description"],
                "meta": {
                        "license": {
                        "id": "ODbL-1.0",
                        "name": data["meta_license_name"] if data["meta_license_name"]!="" else "license name"
                        }
                    },
           }
           result = self.api.put(urlpath, payload=payload)
        except APIError as err:
            messages.error(self.request, err)
            return super(IndexProductView, self).form_invalid(form)
        except Exception as err:
            messages.error(self.request, "Unknown Error")
            return super(IndexProductView, self).form_invalid(form)
        if 'code' in result and result['code']>=400:
            messages.error(self.request, result['message'])
            return super(IndexProductView, self).form_valid(form)
        msg = 'Product {} for Bank {} has been created successfully!'.format(result['product_code'], result['bank_id'])
        messages.success(self.request, msg)
        return super(IndexProductView, self).form_valid(form)

class UpdateProductView(LoginRequiredMixin, FormView):
    template_name = "products/update.html"
    success_url = '/products/list'
    form_class = CreateProductForm

    def dispatch(self, request, *args, **kwargs):
        self.api = API(request.session.get('obp'))
        return super(UpdateProductView, self).dispatch(request, *args, **kwargs)

    def get_form(self, *args, **kwargs):
        form = super(UpdateProductView, self).get_form(*args, **kwargs)
        # Cannot add api in constructor: super complains about unknown kwarg
        form.api = self.api
        fields = form.fields
        urlpath = "/banks/{}/products/{}".format(self.kwargs['bank_id'], self.kwargs['product_code'])
        try:
            fields['bank_id'].choices = self.api.get_bank_id_choices()
        except APIError as err:
            messages.error(self.request, err)
        except Exception as err:
            messages.error(self.request, err)
        try:
            result = self.api.get(urlpath)
            fields['parent_product_code'].initial = self.kwargs['parent_product_code']
            fields['name'].initial = result['name']
            fields['more_info_url'].initial = result['more_info_url']
            fields['terms_and_conditions_url'].initial = result['terms_and_conditions_url']
            fields['description'].initial = result['description']
            fields['meta_license_id'].initial = result['meta']['license']['id']
            fields['meta_license_name'].initial = result['meta']['license']['name']
        except APIError as err:
            messages.error(self.request, err)
        except Exception as err:
            messages.error(self.request, "Unknown Error {}".format(err))
        return form
    def form_valid(self, form):
        data = form.cleaned_data
        urlpath = '/banks/{}/products/{}'.format(data["bank_id"], data["product_code"])
        payload = {
            #"product_code": data["product_code"],
            "parent_product_code": data["parent_product_code"],
            #"bank_id": data["bank_id"],
            "name": data["name"],
            "more_info_url": data["more_info_url"],
            "terms_and_conditions_url": data["terms_and_conditions_url"],
            "description": data["description"],
            "meta": {
                "license": {
                    "id": "PDDL",
                    "name": data["meta_license_name"] if data["meta_license_name"]!="" else "license name"
                }
            },
        }
        try:
            result = self.api.put(urlpath, payload=payload)
            print(result, "This is result")
            if 'code' in result and result['code']>=400:
                error_once_only(self.request, result['message'])
                return super(UpdateProductView, self).form_invalid(form)
        except APIError as err:
            messages.error(self.request, err)
            return super(UpdateProductView, self).form_invalid(form)
        except Exception as err:
            messages.error(self.request, err)
            return super(UpdateProductView, self).form_invalid(form)
        msg = 'Product {} for Bank {} has been Update successfully!'.format(  # noqa
            data["product_code"], data["bank_id"])
        messages.success(self.request, msg)
        return super(UpdateProductView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(UpdateProductView, self).get_context_data(**kwargs)
        self.bank_id = self.kwargs['bank_id']
        self.branch_id = self.kwargs['product_code']
        context.update({
            'product_code': self.product_code,
            'bank_id': self.bank_id
        })
        return context


@exception_handle
@csrf_exempt
def create_list(request):
    print(request.POST, "createProductList listt")
    return HttpResponse("<h1>View 1</h1>")

