
from django.shortcuts import render

# Create your views here.
# -*- coding: utf-8 -*-
"""
Views of atms app
"""
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
import json
from django.urls import reverse_lazy
from django.views.generic import FormView
from obp.api import API, APIError
from .forms import CreateAtmForm
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse, reverse_lazy
from base.utils import exception_handle, error_once_only
from django.conf import settings

CHOOSE = "Choose..."

class IndexAtmsView(LoginRequiredMixin, FormView):

    """Index view for ATMs"""
    template_name = "atms/index.html"
    form_class = CreateAtmForm
    success_url = reverse_lazy('atms_create')

    def dispatch(self, request, *args, **kwargs):
        self.api = API(request.session.get('obp'))
        return super(IndexAtmsView, self).dispatch(request, *args, **kwargs)

    def get_form(self, *args, **kwargs):
        form = super(IndexAtmsView, self).get_form(*args, **kwargs)
        # Cannot add api in constructor: super complains about unknown kwarg
        form.api = self.api
        fields = form.fields
        try:
            fields['bank_id'].choices = self.api.get_bank_id_choices()
            fields['is_accessible'].choices = [('',_(CHOOSE)),(True, True), (False, False)]
            fields['has_deposit_capability'].choices = [('',_(CHOOSE)),(True, True), (False, False)]
            fields['lobby'].initial = json.dumps({
                            "monday": [
                                {
                                    "opening_time": "",
                                    "closing_time": ""
                                }
                            ],
                            "tuesday": [
                                {
                                    "opening_time": "",
                                    "closing_time": ""
                                }
                            ],
                            "wednesday": [
                                {
                                    "opening_time": "",
                                    "closing_time": ""
                                }
                            ],
                            "thursday": [
                                {
                                    "opening_time": "",
                                    "closing_time": ""
                                }
                            ],
                            "friday": [
                                {
                                    "opening_time": "",
                                    "closing_time": ""
                                }
                            ],
                            "saturday": [
                                {
                                    "opening_time": "",
                                    "closing_time": ""
                                }
                            ],
                            "sunday": [
                                {
                                    "opening_time": "",
                                    "closing_time": ""
                                }
                            ]
                        }, indent=4)

            fields['address'].initial = json.dumps({
                "line_1":"No 1 the Road",
                "line_2":"The Place",
                "line_3":"The Hill",
                "city":"Berlin",
                "county":"String",
                "state":"Brandenburg",
                "postcode":"13359",
                "country_code":"DE"
            }, indent=4)
        except APIError as err:
            messages.error(self.request, err)
        except Exception as err:
            messages.error(self.request, err)

        return form

    # Form Valid, when create a new ATM
    def form_valid(self, form):
        try:
            data = form.cleaned_data
            urlpath = '/banks/{}/atms'.format(data['bank_id'])
            payload ={
                "id": data["atm_id"],
                "bank_id": data["bank_id"],
                "name": data["name"],
                "address": json.loads(data['address']),
                "location": self._location(data),
                "meta": self._meta(data),
                "monday": {
                    "opening_time": "",
                    "closing_time": ""
                },
                "tuesday": {
                    "opening_time": "",
                    "closing_time": ""
                },
                "wednesday": {
                    "opening_time": "",
                    "closing_time": ""
                },
                "thursday": {
                    "opening_time": "",
                    "closing_time": ""
                },
                "friday": {
                    "opening_time": "",
                    "closing_time": ""
                },
                "saturday": {
                    "opening_time": "",
                    "closing_time": ""
                },
                "sunday": {
                    "opening_time": "",
                    "closing_time": ""
                },
                "supported_languages":[data["supported_languages"]],
                "services":[data["services"]],
                "accessibility_features":[data["accessibility_features"]],
                "supported_currencies":[data["supported_currencies"]],
                "notes":[data["notes"]],
                "location_categories":[data["location_categories"]],
                **self._boolean_payload1(data),
                **self._boolean_payload2(data),

            }
            result = self.api.post(urlpath, payload=payload)
        except APIError as err:
            messages.error(self.request, err)
            return super(IndexAtmsView, self).form_invalid(form)
        except Exception as err:
            messages.error(self.request, err)
            return super(IndexAtmsView, self).form_invalid(form)
        if 'code' in result and result['code']>=400:
            messages.error(self.request, result['message'])
            return super(IndexAtmsView, self).form_valid(form)
        msg = 'atm {} for Bank {} has been created successfully!'.format(result["id"],result['bank_id'])
        messages.success(self.request, msg)
        return super(IndexAtmsView, self).form_valid(form)

    def _location(self, data):
        return  {
            "latitude": float(data["location_latitude"]) if data["location_latitude"] is not None else "",
            "longitude": float(data["location_longitude"]) if data["location_longitude"] is not None else ""
        }

    def _meta(self, data):
        return {
            "license": {
            "id": "ODbL-1.0",
            "name": data["meta_license_name"] if data["meta_license_name"]!="" else "license name"
            }
        }

    def _boolean_payload1(self, data):
        return {
            "is_accessible": data["is_accessible"] if data["is_accessible"]!="" else "false",
            "located_at": data["located_at"] if data["located_at"]!="no-example-provided" else " ",
            "more_info": data["more_info"] if data["more_info"]!="" else "false",
            "has_deposit_capability": data["has_deposit_capability"] if data["has_deposit_capability"]!="" else "false",
            "minimum_withdrawal": data["minimum_withdrawal"] if data["minimum_withdrawal"]!="" else "false"
        }

    def _boolean_payload2(self, data):
        return {
            "branch_identification": data["branch_identification"] if data["branch_identification"]!="" else "false",
            "site_identification": data["site_identification"] if data["site_identification"]!="" else "false",
            "site_name": data["site_name"] if data["site_name"]!="" else "false",
            "cash_withdrawal_national_fee": data["cash_withdrawal_national_fee"] if data["cash_withdrawal_national_fee"]!="" else "false",
            "cash_withdrawal_international_fee": data["cash_withdrawal_international_fee"] if data["cash_withdrawal_international_fee"]!="" else "false",
            "balance_inquiry_fee": data["balance_inquiry_fee"] if data["balance_inquiry_fee"]!="" else "false"
        }

class UpdateAtmsView(LoginRequiredMixin, FormView):
    template_name = "atms/update.html"
    success_url = '/atms/list'
    form_class = CreateAtmForm
    v510 = settings.API_ROOT['v510']

    def dispatch(self, request, *args, **kwargs):
        self.api = API(request.session.get('obp'))
        return super(UpdateAtmsView, self).dispatch(request, *args, **kwargs)

    def get_form(self, *args, **kwargs):
        form = super(UpdateAtmsView, self).get_form(*args, **kwargs)
        # Cannot add api in constructor: super complains about unknown kwarg
        form.api = self.api
        fields = form.fields
        urlpath = "/banks/{}/atms/{}".format(self.kwargs['bank_id'], self.kwargs['atm_id']) #Add new attribute urlpath
        atm_attributes_url_path = "/banks/{}/atms/{}/attributes".format(self.kwargs['bank_id'], self.kwargs['atm_id'])

        try:
            fields['bank_id'].choices = self.api.get_bank_id_choices()
        except APIError as err:
            messages.error(self.request, err)
        except Exception as err:
            messages.error(self.request, err)
        try:
            result = self.api.get(urlpath)
            fields['bank_id'].initial = self.kwargs['bank_id']
            fields['atm_id'].initial = self.kwargs['atm_id']
            fields['name'].initial = result['name']
            fields['address'].initial = json.dumps(result['address'], indent=4)
            fields['location_latitude'].initial = result['location']['latitude']
            fields['location_longitude'].initial = result['location']['longitude']
            fields['meta_license_id'].initial = result['meta']['license']['id']
            fields['meta_license_name'].initial = result['meta']['license']['name']
            fields['minimum_withdrawal'].initial = result['minimum_withdrawal']
            fields['branch_identification'].initial = result['branch_identification']
            fields['site_identification'].initial = result['site_identification']
            fields['site_name'].initial = result['site_name']
            fields['cash_withdrawal_national_fee'].initial = result['cash_withdrawal_national_fee']
            fields['cash_withdrawal_international_fee'].initial = result['cash_withdrawal_international_fee']
            fields['balance_inquiry_fee'].initial = result['balance_inquiry_fee']
            my_services = result["services"]
            services_initial = ','.join(my_services)
            fields['services'].initial = services_initial

            fields['more_info'].initial = result['more_info']
            fields['located_at'].initial = result['located_at']

            my_notes = result["notes"]
            note_initial = ','.join(my_notes)
            fields['notes'].initial = note_initial

            my_location_categories = result['location_categories']
            location_categories_initial = ','.join(my_location_categories)
            fields['location_categories'].initial = location_categories_initial

            my_supported_currencies = result['supported_currencies']
            supported_currencies_initial = ','.join(my_supported_currencies)
            fields['supported_currencies'].initial = supported_currencies_initial

            my_supported_languages = result['supported_languages']
            supported_languages_initial = ','.join(my_supported_languages)
            fields['supported_languages'].initial = supported_languages_initial

            my_accessibility_features = result['accessibility_features']
            my_accessibility_features_initial = ','.join(my_accessibility_features)
            fields['accessibility_features'].initial = my_accessibility_features_initial
            self._payload_choices(result, fields)
        except Exception as err:
            messages.error(self.request, "Unknown Error {}".format(err))
        return form

    def _payload_choices(self, result, fields):
        if result['is_accessible'].lower()=='true':
            fields['is_accessible'].choices = [(True, True), (False, False)]
        else:
            fields['is_accessible'].choices = [(False, False), (True, True)]
        if result['has_deposit_capability'].lower()=='true':
            fields['has_deposit_capability'].choices = [(True, True), (False, False)]
        else:
            fields['has_deposit_capability'].choices = [(False, False), (True, True)]

    #Check form validation, when update previous ATM
    def form_valid(self, form):
        data = form.cleaned_data
        urlpath = '/banks/{}/atms/{}'.format(data["bank_id"],data["atm_id"])
        payload = {
            "id": data["atm_id"],
            "bank_id": data["bank_id"],
            "name": data["name"],
            "address": json.loads(data['address']),
            "location": {
                "latitude": float(data["location_latitude"]) if data["location_latitude"] is not None else "",
                "longitude": float(data["location_longitude"]) if data["location_longitude"] is not None else ""
            },
            "meta": {
                "license": {
                "id": "ODbL-1.0",
                "name": data["meta_license_name"] if data["meta_license_name"]!="" else "license name"
                }
            },
            "monday": {
                "opening_time": " ",
                "closing_time": " "
            },
            "tuesday": {
                "opening_time": " ",
                "closing_time": " "
            },
            "wednesday": {
                "opening_time": " ",
                "closing_time": " "
            },
            "thursday": {
                "opening_time": " ",
                "closing_time": " "
            },
            "friday": {
                "opening_time": " ",
                "closing_time": " "
            },
            "saturday": {
                "opening_time": " ",
                "closing_time": " "
            },
            "sunday": {
                "opening_time": " ",
                "closing_time": " "
            },
            "supported_languages":[data["supported_languages"]],
            "services":[data["services"]],
            "accessibility_features":[data["accessibility_features"]],
            "supported_currencies":[data["supported_currencies"]],
            "notes":[data["notes"]],
            "location_categories":[data["location_categories"]],
            **self._update_boolean_payload1(data),
            **self._update_boolean_payload2(data)
        }
        try:
            result = self.api.put(urlpath, payload=payload)
            if 'code' in result and result['code']>=400:
                messages.error(self.request, result['message'])
                return super(UpdateAtmsView, self).form_invalid(form)
        except APIError as err:
            messages.error(self.request, err)
            return super(UpdateAtmsView, self).form_invalid(form)
        except Exception as e:
            messages.error(self.request, e)
            return super(UpdateAtmsView, self).form_invalid(form)
        msg = 'Atm {} for Bank {} has been updated successfully!'.format(  # noqa
            data["atm_id"], data["bank_id"])
        messages.success(self.request, msg)
        return super(UpdateAtmsView, self).form_valid(form)

    def _update_boolean_payload1(self, data):
        return {
            "is_accessible": data["is_accessible"] if data["is_accessible"]!="" else "false",
            "located_at": data["located_at"] if data["located_at"]!="no-example-provided" else " ",
            "more_info": data["more_info"] if data["more_info"]!="" else "false",
            "has_deposit_capability": data["has_deposit_capability"] if data["has_deposit_capability"]!="" else "false",
            "minimum_withdrawal": data["minimum_withdrawal"] if data["minimum_withdrawal"]!="" else "false"
        }

    def _update_boolean_payload2(self, data):
        return {
            "branch_identification": data["branch_identification"] if data["branch_identification"]!="" else "false",
            "site_identification": data["site_identification"] if data["site_identification"]!="" else "false",
            "site_name": data["site_name"] if data["site_name"]!="" else "false",
            "cash_withdrawal_national_fee": data["cash_withdrawal_national_fee"] if data["cash_withdrawal_national_fee"]!="" else "false",
            "cash_withdrawal_international_fee": data["cash_withdrawal_international_fee"] if data["cash_withdrawal_international_fee"]!="" else "false",
            "balance_inquiry_fee": data["balance_inquiry_fee"] if data["balance_inquiry_fee"]!="" else "false"
        }

    def atm_attributes(self, **kwargs):
        atm_attributes_url_path = "/banks/{}/atms/{}/attributes".format(self.kwargs['bank_id'], self.kwargs['atm_id'])
        try:
            atm_attributes_result = self.api.get(atm_attributes_url_path, version=self.v510)["atm_attributes"]
            return atm_attributes_result
        except Exception as err:
            messages.error(self.request, "Unknown Error {}".format(err))
        return " "


    def get_context_data(self, **kwargs):
        context = super(UpdateAtmsView, self).get_context_data(**kwargs)
        self.bank_id = self.kwargs['bank_id']
        self.atm_id = self.kwargs['atm_id']
        context.update({
            'atm_id': self.atm_id,
            'bank_id': self.bank_id,
            "atm_attributes_list": self.atm_attributes(**kwargs)
        })
        return context


@exception_handle
@csrf_exempt
def atm_attribute_save(request):
    api = API(request.session.get('obp'))
    #urlpath = '/my/api-collections'
    bank_id = request.POST.get('bank_id').strip()
    atm_id = request.POST.get('atm_id').strip()
    urlpath_save = '/banks/{}/atms/{}/attributes'.format(bank_id, atm_id)

    payload = {
        'name': request.POST.get('name').strip(),
        'type': request.POST.get('type').strip(),
        'value': request.POST.get('value').strip(),
        'is_active': True
    }
    result = api.post(urlpath_save, payload = payload, version=settings.API_ROOT['v510'])
    return result


@exception_handle
@csrf_exempt
def atm_attribute_update(request):
    bank_id = request.POST.get('bank_id').strip()
    atm_id = request.POST.get('atm_id').strip()
    atm_attribute_id = request.POST.get('atm_attribute_id').strip()
    api = API(request.session.get('obp'))
    urlpath_update = '/banks/{}/atms/{}/attributes/{}'.format(bank_id, atm_id, atm_attribute_id)
    payload = {
        'name': request.POST.get('name').strip(),
        'type': request.POST.get('type').strip(),
        'value': request.POST.get('value').strip(),
        'is_active': True
    }
    result = api.put(urlpath_update, payload=payload, version=settings.API_ROOT['v510'])
    return result


@exception_handle
@csrf_exempt
def atm_attribute_delete(request):
    bank_id = request.POST.get('bank_id').strip()
    atm_id = request.POST.get('atm_id').strip()
    atm_attribute_id = request.POST.get('atm_attribute_id').strip()

    api = API(request.session.get('obp'))
    urlpath_delete = '/banks/{}/atms/{}/attributes/{}'.format(bank_id, atm_id, atm_attribute_id)
    result = api.delete(urlpath_delete, version=settings.API_ROOT['v510'])
    return result



