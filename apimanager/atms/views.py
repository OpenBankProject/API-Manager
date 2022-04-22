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

class IndexAtmsView(LoginRequiredMixin, FormView):
    """Index view for ATMs"""
    template_name = "atms/index.html"
    form_class = CreateAtmForm
    success_url = reverse_lazy('atms_list')

    def dispatch(self, request, *args, **kwargs):
        self.api = API(request.session.get('obp'))
        return super(IndexAtmsView, self).dispatch(request, *args, **kwargs)

    def get_form(self, *args, **kwargs):
        form = super(IndexAtmsView, self).get_form(*args, **kwargs)
        # Cannot add api in constructor: super complains about unknown kwarg
        form.api = self.api
        fields = form.fields
        try:

            #fields["atm_id"]=
            fields['bank_id'].choices = self.api.get_bank_id_choices()
            fields['is_accessible'].choices = [('','Choose...'),(True, True), (False, False)]
            fields['has_deposit_capability'].choices = [('','Choose...'),(True, True), (False, False)]
            fields['supported_languages'].choices = [('','Choose...'),("en", "en"), ("fr", "fr"), ("de", "de")]
            fields['notes'].choices = [('','Choose...'),("String1", "String1"), ("String2", "String2")]
            fields['supported_currencies'].choices = [('','Choose...'),("EUR", "EUR"), ("MXN", "MXN"), ("USD", "USD")]
            fields['location_categories'].choices = [('','Choose...'),("ATBI", "ATBI"), ("ATBE", "ATBE")]
            #fields['lobby'].initial = json.dumps({
            fields["monday"].initial=json.dumps({"opening_time": "10:00","closing_time": "18:00"})
            fields["tuesday"].initial=json.dumps({"opening_time": "10:00","closing_time": "18:00"})
            fields["wednesday"].initial=json.dumps({"opening_time": "10:00","closing_time": "18:00"})
            fields["thursday"].initial=json.dumps({"opening_time": "10:00","closing_time": "18:00"})
            fields["friday"].initial=json.dumps({"opening_time": "10:00","closing_time": "18:00"})
            fields["saturday"].initial=json.dumps({"opening_time": "10:00","closing_time": "18:00"})
            fields["sunday"].initial=json.dumps({"opening_time": "10:00","closing_time": "18:00"})
            #}, indent=4)

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

    def form_valid(self, form):
        try:
            data = form.cleaned_data
            #print(data["id"], "This is a id from data")
            urlpath = '/banks/{}/atms'.format(data['bank_id'])
            print(data["atm_id"], "This is a atm_id")
            payload = {
               "id": data["atm_id"],
                "bank_id": data["bank_id"],
                "name": data["name"],
                "address": json.loads(data['address']),
                "location": {
                    "latitude": float(data["location_latitude"]) if data["location_latitude"] is not None else 37.0,
                    "longitude": float(data["location_longitude"]) if data["location_longitude"] is not None else 110.0
                },
                "meta": {
                    "license": {
                        "id": "PDDL",
                        "name": data["meta_license_name"] if data["meta_license_name"]!="" else "license name"
                    }
                },
                "monday":data["monday"] if data["monday"]!= "" else "false",
                "tuesday":data["tuesday"] if data["tuesday"]!= "" else "false",
                "wednesday":data["wednesday"] if data["wednesday"]!= "" else "false",
                "thursday":data["thursday"] if data["thursday"]!= "" else "false",
                "friday":data["friday"] if data["friday"]!= "" else "false",
                "saturday":data["saturday"] if data["saturday"]!= "" else "false",
                "sunday":data["sunday"] if data["sunday"]!= "" else "false",
                "is_accessible": data["is_accessible"] if data["is_accessible"]!="" else "false",
                "has_deposit_capability": data["has_deposit_capability"] if data["has_deposit_capability"]!="" else "false",
                "supported_languages": data["supported_languages"] if data["supported_languages"]!="" else "false",
                "supported_currencies": data["supported_currencies"] if data["supported_currencies"]!="" else "false",
                "notes": data["notes"] if data["notes"]!="" else "false",
                "location_categories": data["location_categories"] if data["location_categories"]!="" else "false",
                "accessible_features": data["accessibleFeatures"] if data["accessibleFeatures"]!="" else "false",
                "minimum_withdrawal": data["minimum_withdrawal"] if data["minimum_withdrawal"]!="" else "false",
                "branch_identification": data["branch_identification"] if data["branch_identification"]!="" else "false",
                "site_identification": data["site_identification"] if data["site_identification"]!="" else "false",
                "site_name": data["site_name"] if data["site_name"]!="" else "false",
                "cash_withdrawal_national_fee": data["cash_withdrawal_national_fee"] if data["cash_withdrawal_national_fee"]!="" else "false",
                "cash_withdrawal_international_fee": data["cash_withdrawal_international_fee"] if data["cash_withdrawal_international_fee"]!="" else "false",
                "balance_inquiry_fee": data["balance_inquiry_fee"] if data["balance_inquiry_fee"]!="" else "false",
                "more_info": data["more_info"] if data["more_info"]!="" else "false",
                "located_at": data["located_at"] if data["located_at"]!="" else "false",
                "services": data["services"] if data["services"]!="" else "false",
            }
            #payload=json.dumps(payload)
            result = self.api.post(urlpath, payload=payload)
            print(result, "Hello World")
        except APIError as err:
            messages.error(self.request, err)
            return super(IndexAtmsView, self).form_invalid(form)
        except Exception as err:
            messages.error(self.request, err)
            return super(IndexAtmsView, self).form_invalid(form)
        if 'code' in result and result['code']>=400:
            messages.error(self.request, "result Unknown Error")
            print(result, "Result is")
            return super(IndexAtmsView, self).form_valid(form)
        #msg = ("Record has been created successfully!")
        msg = 'atm {} for Bank {} has been created successfully!', result['bank_id']
        messages.success(self.request, msg)
        return super(IndexAtmsView, self).form_valid(form)

    def get_banks(self):
        api = API(self.request.session.get('obp'))
        try:
            urlpath = '/banks'
            result = api.get(urlpath)
            print(result, "get_banks")
            if 'banks' in result:
                return [bank['id'] for bank in sorted(result['banks'], key=lambda d: d['id'])]
            else:
                return []
        except APIError as err:
            messages.error(self.request, err)
            return []

    def get_atms(self, context):

        api = API(self.request.session.get('obp'))
        try:
            self.bankids = self.get_banks()
            atms_list = []
            for bank_id in self.bankids:
                urlpath = '/banks/{}/atms'.format(bank_id)

                result = api.get(urlpath)
                print(result,"get_atms")
                if 'atms' in result:
                    atms_list.extend(result['atms'])
        except APIError as err:
            messages.error(self.request, err)
            return []
        except Exception as inst:
            messages.error(self.request, "Unknown Error {}".format(type(inst).__name__))
            return []

        return atms_list

    def get_context_data(self, **kwargs):
        context = super(IndexAtmsView, self).get_context_data(**kwargs)
        atms_list = self.get_atms(context)
        context.update({
            'atms_list': atms_list,
            'bankids': self.bankids
        })
        return context


class UpdateAtmsView(LoginRequiredMixin, FormView):
    template_name = "atms/update.html"
    success_url = '/atms/'
    form_class = CreateAtmForm

    def dispatch(self, request, *args, **kwargs):
        self.api = API(request.session.get('obp'))
        return super(UpdateAtmsView, self).dispatch(request, *args, **kwargs)

    def get_form(self, *args, **kwargs):
        form = super(UpdateAtmsView, self).get_form(*args, **kwargs)
        # Cannot add api in constructor: super complains about unknown kwarg
        form.api = self.api
        fields = form.fields
        urlpath = "/banks/{}/atms/{}".format(self.kwargs['bank_id'], self.kwargs['atm_id'])
        try:
            fields['bank_id'].choices = self.api.get_bank_id_choices()

        except APIError as err:
            messages.error(self.request, err)
        except:
            messages.error(self.request, "Unknown Error")
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
            if result['is_accessible'].lower()=='true':
                fields['is_accessible'].choices = [(True, True), (False, False)]
            else:
                fields['is_accessible'].choices = [(False, False), (True, True)]
            if result['has_deposit_capability'].lower()=='true':
                fields['has_deposit_capability'].choices = [(True, True), (False, False)]
            else:
                fields['has_deposit_capability'].choices = [(False, False), (True, True)]
            fields['has_deposit_capability'].initial = result['accessibleFeatures']
            fields['site_identification'].initial = result['site_identification']
            fields['site_name'].initial = result['site_name']
            fields['cash_withdrawal_national_fee'].initial = result['cash_withdrawal_national_fee']
            fields['cash_withdrawal_international_fee'].initial = result['cash_withdrawal_international_fee']
            fields['balance_inquiry_fee'].initial = result['balance_inquiry_fee']
            fields['services'].initial = result['services']
            fields['located_at'].initial = result['located_at']
            fields['more_info'].initial = result['more_info']
            fields['located_at'].initial = result['located_at']
            fields['lobby'].initial = json.dumps(result['lobby'], indent=4)
            if result['supported_languages'].lower()=='en':
                fields['supported_languages'].choices = [("en", "en"), ("fr", "fr"), ("de", "de")]
            elif result['supported_languages'].lower()=='fr':
                fields['supported_languages'].choices = [("fr", "fr"), ("en", "en"), ("de", "de")]
            else:
                fields['supported_languages'].choices = [("de", "de"),("fr", "fr"), ("en", "en")]
            fields['supported_languages'].initial = result['supported_languages']
            if result['supported_currencies'].lower()=='eur':
                  fields['supported_currencies'].choices = [("EUR", "EUR"), ("MXN", "MXN"), ("USD", "USD")]
            elif result['supported_currencies'].lower()=='mxn':
                  fields['supported_currencies'].choices = [("MXN", "MXN"), ("EUR", "EUR"), ("USD", "USD")]
            else:
                  fields['supported_currencies'].choices = [("USD", "USD"),("MXN", "MXN"), ("EUR", "EUR")]
            fields['supported_currencies'].initial = result['supported_currencies']
            if result['notes'].lower()=='string1':
                  fields['notes'].choices = [("String1", "String1"),("String2", "String2")]
            else:
                  fields['notes'].choices = [("String2", "String2"),("String1", "String1")]
            fields['notes'].initial = result['notes']
            if result['location_categories'].lower()=='atbi':
                 fields['location_categories'].choices = [("ATBI", "ATBI"),("ATBE", "ATBE")]
            else:
                 fields['location_categories'].choices = [("ATBE", "ATBE"),("ATBI", "ATBI")]
            fields['location_categories'].initial = result['location_categories']
        except APIError as err:
            messages.error(self.request, err)
        except Exception as err:
            messages.error(self.request, "Unknown Error {}".format(err))

        return form

    def form_valid(self, form):
        data = form.cleaned_data
        urlpath = '/banks/{}/atms/{}'.format(data["bank_id"],data["atm_id"])
        payload = {
            "id": data["atm_id"],
            "bank_id": data["bank_id"],
            "name": data["name"],
            "address": json.loads(data['address']),
            "location": {
                "latitude": float(data["location_latitude"]),
                "longitude": float(data["location_longitude"])
            },
            "meta": {
                "license": {
                    "id": data["meta_license_id"],
                    "name": data["meta_license_name"]
                }
            },
            "lobby": json.loads(data["lobby"]),
            "has_deposit_capability": data["has_deposit_capability"],
            "accessibleFeatures": data["accessibleFeatures"],
            "minimum_withdrawal": data["minimum_withdrawal"],
            "branch_identification": data["branch_identification"],
            "site_identification": data["site_identification"],
            "site_name": data["site_name"],
            "cash_withdrawal_national_fee": data["cash_withdrawal_national_fee"],
            "cash_withdrawal_international_fee": data["cash_withdrawal_international_fee"],
            "balance_inquiry_fee": data["balance_inquiry_fee"],
            "services": data["services"],
            "more_info": data["more_info"],
            "located_at": data["located_at"],
            "phone_number": data["phone_number"],
            "supported_languages": data["supported_languages"],
            "supported_currencies": data["supported_currencies"],
            "notes": data["notes"],
            "location_categories": data["location_categories"]
        }
        try:
            result = self.api.put(urlpath, payload=payload)
            if 'code' in result and result['code']>=400:
                error_once_only(self.request, result['message'])
                return super(UpdateAtmsView, self).form_invalid(form)
        except APIError as err:
            messages.error(self.request, err)
            return super(UpdateAtmsView, self).form_invalid(form)
        except:
            messages.error(self.request, "Unknown Error")
            return super(UpdateAtmsView, self).form_invalid(form)
        msg = 'Atm {} for Bank {} has been created successfully!'.format(  # noqa
            data["atm_id"], data["bank_id"])
        messages.success(self.request, msg)
        return super(UpdateAtmsView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(UpdateAtmsView, self).get_context_data(**kwargs)
        self.bank_id = self.kwargs['bank_id']
        self.atm_id = self.kwargs['atm_id']
        context.update({
            'atm_id': self.atm_id,
            'bank_id': self.bank_id
        })
        return context
