from django.shortcuts import render

# Create your views here.
# -*- coding: utf-8 -*-
"""
Views of branches app
"""

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
import json
from django.urls import reverse_lazy
from django.views.generic import FormView

from obp.api import API, APIError

from .forms import CreateBranchForm


def error_once_only(request, err):
    """
    Just add the error once
    :param request:
    :param err:
    :return:
    """
    storage = messages.get_messages(request)
    if str(err) not in [str(m.message) for m in storage]:
        messages.error(request, err)


class IndexBranchesView(LoginRequiredMixin, FormView):
    """Index view for branches"""
    template_name = "branches/index.html"
    form_class = CreateBranchForm
    success_url = reverse_lazy('branches_list')

    def dispatch(self, request, *args, **kwargs):
        self.api = API(request.session.get('obp'))
        return super(IndexBranchesView, self).dispatch(request, *args, **kwargs)

    def get_form(self, *args, **kwargs):
        form = super(IndexBranchesView, self).get_form(*args, **kwargs)
        # Cannot add api in constructor: super complains about unknown kwarg
        form.api = self.api
        fields = form.fields
        try:
            fields['bank_id'].choices = self.api.get_bank_id_choices()
            fields['is_accessible'].choices = [('','Choose...'),(True, True), (False, False)]
            fields['drive_up'].initial = json.dumps({
                "monday": {
                    "opening_time": "10:00",
                    "closing_time": "18:00"
                },
                "tuesday": {
                    "opening_time": "10:00",
                    "closing_time": "18:00"
                },
                "wednesday": {
                    "opening_time": "10:00",
                    "closing_time": "18:00"
                },
                "thursday": {
                    "opening_time": "10:00",
                    "closing_time": "18:00"
                },
                "friday": {
                    "opening_time": "10:00",
                    "closing_time": "18:00"
                },
                "saturday": {
                    "opening_time": "10:00",
                    "closing_time": "18:00"
                },
                "sunday": {
                    "opening_time": "10:00",
                    "closing_time": "18:00"
                }
            }, indent=4)

            fields['lobby'].initial = json.dumps({
                "monday": [
                    {
                        "opening_time": "10:00",
                        "closing_time": "18:00"
                    }
                ],
                "tuesday": [
                    {
                        "opening_time": "10:00",
                        "closing_time": "18:00"
                    }
                ],
                "wednesday": [
                    {
                        "opening_time": "10:00",
                        "closing_time": "18:00"
                    }
                ],
                "thursday": [
                    {
                        "opening_time": "10:00",
                        "closing_time": "18:00"
                    }
                ],
                "friday": [
                    {
                        "opening_time": "10:00",
                        "closing_time": "18:00"
                    }
                ],
                "saturday": [
                    {
                        "opening_time": "10:00",
                        "closing_time": "18:00"
                    }
                ],
                "sunday": [
                    {
                        "opening_time": "10:00",
                        "closing_time": "18:00"
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
        except:
            messages.error(self.request, "Unknown Error")

        return form

    def form_valid(self, form):
        try:
            data = form.cleaned_data
            urlpath = '/banks/{}/branches'.format(data['bank_id'])
            payload = {
                "id": data["branch_id"],
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
                "lobby": json.loads(data['lobby']),
                "drive_up": json.loads(data["drive_up"]),
                "branch_routing": {
                    "scheme": data["branch_routing_scheme"] if data["branch_routing_scheme"]!="" else "license name",
                    "address": data["branch_routing_address"] if data["branch_routing_address"]!="" else "license name"
                },
                "is_accessible": data["is_accessible"] if data["is_accessible"]!="" else "false",
                "accessibleFeatures": data["accessibleFeatures"] if data["accessibleFeatures"]!="" else "accessible features name",
                "branch_type": data["branch_type"] if data["branch_type"]!="" else "branch type",
                "more_info": data["more_info"] if data["more_info"]!="" else "more info",
                "phone_number": data["phone_number"] if data["phone_number"]!="" else "phone number"
            }
            result = self.api.post(urlpath, payload=payload)
        except APIError as err:
            error_once_only(self.request, err)
            return super(IndexBranchesView, self).form_invalid(form)
        except Exception as err:
            error_once_only(self.request, "Unknown Error")
            return super(IndexBranchesView, self).form_invalid(form)
        if 'code' in result and result['code']>=400:
            error_once_only(self.request, result['message'])
            return super(IndexBranchesView, self).form_valid(form)
        msg = 'Branch {} for Bank {} has been created successfully!'.format(result['id'], result['bank_id'])
        messages.success(self.request, msg)
        return super(IndexBranchesView, self).form_valid(form)

    def get_banks(self):
        api = API(self.request.session.get('obp'))
        try:
            urlpath = '/banks'
            result = api.get(urlpath)
            if 'banks' in result:
                return [bank['id'] for bank in result['banks']]
            else:
                return []
        except APIError as err:
            messages.error(self.request, err)
            return []

    def get_branches(self, context):

        api = API(self.request.session.get('obp'))
        try:
            self.bankids = self.get_banks()
            branches_list = []
            for bank_id in self.bankids:
                urlpath = '/banks/{}/branches'.format(bank_id)

                result = api.get(urlpath)
                if 'branches' in result:
                    branches_list.extend(result['branches'])
        except APIError as err:
            messages.error(self.request, err)
            return []
        except Exception as inst:
            messages.error(self.request, "Unknown Error {}".format(type(inst).__name__))
            return []

        return branches_list

    def get_context_data(self, **kwargs):
        context = super(IndexBranchesView, self).get_context_data(**kwargs)
        branches_list = self.get_branches(context)
        context.update({
            'branches_list': branches_list,
            'bankids': self.bankids
        })
        return context


class UpdateBranchesView(LoginRequiredMixin, FormView):
    template_name = "branches/update.html"
    success_url = '/branches/'
    form_class = CreateBranchForm

    def dispatch(self, request, *args, **kwargs):
        self.api = API(request.session.get('obp'))
        return super(UpdateBranchesView, self).dispatch(request, *args, **kwargs)

    def get_form(self, *args, **kwargs):
        form = super(UpdateBranchesView, self).get_form(*args, **kwargs)
        # Cannot add api in constructor: super complains about unknown kwarg
        form.api = self.api
        fields = form.fields
        urlpath = "/banks/{}/branches/{}".format(self.kwargs['bank_id'], self.kwargs['branch_id'])
        try:
            fields['bank_id'].choices = self.api.get_bank_id_choices()

        except APIError as err:
            messages.error(self.request, err)
        except:
            messages.error(self.request, "Unknown Error")
        try:
            result = self.api.get(urlpath)
            fields['bank_id'].initial = self.kwargs['bank_id']
            fields['branch_id'].initial = self.kwargs['branch_id']
            fields['name'].initial = result['name']
            fields['address'].initial = json.dumps(result['address'], indent=4)
            fields['location_latitude'].initial = result['location']['latitude']
            fields['location_longitude'].initial = result['location']['longitude']
            fields['meta_license_id'].initial = result['meta']['license']['id']
            fields['meta_license_name'].initial = result['meta']['license']['name']
            fields['branch_routing_scheme'].initial = result['branch_routing']['scheme']
            fields['branch_routing_address'].initial = result['branch_routing']['address']
            if result['is_accessible'].lower()=='true':
                fields['is_accessible'].choices = [(True, True), (False, False)]
            else:
                fields['is_accessible'].choices = [(False, False), (True, True)]
            fields['accessibleFeatures'].initial = result['accessibleFeatures']
            fields['branch_type'].initial = result['branch_type']
            fields['more_info'].initial = result['more_info']
            fields['phone_number'].initial = result['phone_number']
            fields['lobby'].initial = json.dumps(result['lobby'], indent=4)
            fields['drive_up'].initial = json.dumps(result['drive_up'], indent=4)
        except APIError as err:
            messages.error(self.request, err)
        except Exception as err:
            messages.error(self.request, "Unknown Error {}".format(err))

        return form

    def form_valid(self, form):
        data = form.cleaned_data
        urlpath = '/banks/{}/branches/{}'.format(data["bank_id"], data["branch_id"])
        payload = {
            #"id": data["branch_id"],
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
            "drive_up": json.loads(data["drive_up"]),
            "branch_routing": {
                "scheme": data["branch_routing_scheme"] if data["branch_routing_scheme"] != "" else "license name",
                "address": data["branch_routing_address"] if data["branch_routing_address"] != "" else "license name"
            },
            "is_accessible": data["is_accessible"],
            "accessibleFeatures": data["accessibleFeatures"],
            "branch_type": data["branch_type"],
            "more_info": data["more_info"],
            "phone_number": data["phone_number"]
        }
        try:
            result = self.api.put(urlpath, payload=payload)
            if 'code' in result and result['code']>=400:
                error_once_only(self.request, result['message'])
                return super(UpdateBranchesView, self).form_invalid(form)
        except APIError as err:
            messages.error(self.request, err)
            return super(UpdateBranchesView, self).form_invalid(form)
        except:
            messages.error(self.request, "Unknown Error")
            return super(UpdateBranchesView, self).form_invalid(form)
        msg = 'Branch {} for Bank {} has been created successfully!'.format(  # noqa
            data["branch_id"], data["bank_id"])
        messages.success(self.request, msg)
        return super(UpdateBranchesView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(UpdateBranchesView, self).get_context_data(**kwargs)
        self.bank_id = self.kwargs['bank_id']
        self.branch_id = self.kwargs['branch_id']
        context.update({
            'branch_id': self.branch_id,
            'bank_id': self.bank_id
        })
        return context
