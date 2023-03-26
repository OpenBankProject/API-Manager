# -*- coding: utf-8 -*-
"""
Forms of customers app
"""

from django import forms
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from apimanager.settings import API_FIELD_DATE_FORMAT, API_FIELD_TIME_FORMAT
from bootstrap_datepicker_plus import DatePickerInput, DateTimePickerInput
from datetime import datetime, timedelta
from obp.api import APIError

PLACEHOLDER = "2013-01-22"
PLACEHOLDER1 = "00:00:00"

class CreateCustomerForm(forms.Form):
    bank_id = forms.ChoiceField(
        label=_('Bank'),
        widget=forms.Select(
            attrs={
                'class': 'form-control',
            }
        ),
        choices=[],
    )
    user_id = forms.CharField(
        label=_('User Id'),
        widget=forms.TextInput(
            attrs={
                'placeholder': _('The ID of the user'),
                'class': 'form-control',
            }
        ),
    )
    customer_number = forms.CharField(
        label=_('Customer Number'),
        widget=forms.TextInput(
            attrs={
                'placeholder': 'E.g. `007`',
                'class': 'form-control',
            }
        ),
    )
    legal_name = forms.CharField(
        label=_('Legal Name'),
        widget=forms.TextInput(
            attrs={
                'placeholder': 'NONE',
                'class': 'form-control',
            }
        ),
        required=False,
    )
    mobile_phone_number = forms.CharField(
        label=_('Mobile Phone Number'),
        widget=forms.TextInput(
            attrs={
                'placeholder': _('E.g. +49 123 456 78 90 12'),
                'class': 'form-control',
            }
        ),
        required=False,
    )
    email = forms.CharField(
        label=_('Email'),
        widget=forms.TextInput(
            attrs={
                'placeholder': _('E.g. person@example.com'),
                'class': 'form-control',
            }
        ),
        required=False,
    )
    face_image_url = forms.CharField(
        label=_('Face Image URL'),
        widget=forms.TextInput(
            attrs={
                'placeholder': 'https://static.openbankproject.com/images/OBP/favicon.png',  # noqa
                'class': 'form-control',
            }
        ),
        required=False,
    )
    face_image_date = forms.DateTimeField(
        label=_('Face Image Date'),
        input_formats=[settings.API_DATE_FORMAT_WITH_SECONDS ],
        widget=forms.DateTimeInput(
            attrs={
                'placeholder': PLACEHOLDER,
                'class': 'form-control',
            }
        ),
        required=False,
    )
    date_of_birth_date = forms.DateField(
            label=_("Date of Birth"),
            widget=DatePickerInput(format=API_FIELD_DATE_FORMAT),
            required=True,
            initial=str(datetime.now().strftime(API_FIELD_DATE_FORMAT)),
        )
    date_of_birth_time = forms.TimeField(
        label=_('Time of Birth'),
        widget=forms.TimeInput(
            format='%H:%M:%S',
            attrs={
                'placeholder': PLACEHOLDER1,
                'class': 'form-control',
            }
        ),
        required=False,
    )
    relationship_status = forms.CharField(
        label=_('Relationship Status'),
        widget=forms.TextInput(
            attrs={
                'placeholder': _('Single'),
                'class': 'form-control',
            }
        ),
        required=False,
    )
    dependants = forms.IntegerField(
        label=_('Dependants'),
        widget=forms.TextInput(
            attrs={
                'placeholder': '0',
                'class': 'form-control',
            }
        ),
        initial=0,
        required=True,
    )
    dob_of_dependants = forms.CharField(
        label=_('Date of Birth of Dependants'),
        widget=forms.TextInput(
            attrs={
                'placeholder': f'{PLACEHOLDER}, 2010-01-22T00:08:00Z',
                'class': 'form-control',
            }
        ),
        required=False,
    )
    credit_rating_rating = forms.CharField(
        label=_('Credit Rating (Rating)'),
        widget=forms.TextInput(
            attrs={
                'placeholder': 'OBP',
                'class': 'form-control',
            }
        ),
        required=False,
    )
    credit_rating_source = forms.CharField(
        label=_('Credit Rating (Source)'),
        widget=forms.TextInput(
            attrs={
                'placeholder': 'OBP',
                'class': 'form-control',
            }
        ),
        required=False,
    )
    credit_limit_currency = forms.CharField(
        label=_('Credit Limit (Currency)'),
        widget=forms.TextInput(
            attrs={
                'placeholder': 'EUR',
                'class': 'form-control',
            }
        ),
        required=False,
    )
    credit_limit_amount = forms.CharField(
        label=_('Credit Limit (Amount)'),
        widget=forms.TextInput(
            attrs={
                'placeholder': '10',
                'class': 'form-control',
            }
        ),
        required=False,
    )
    highest_education_attained = forms.CharField(
        label=_('Highest Education Attained'),
        widget=forms.TextInput(
            attrs={
                'placeholder': _('Bachelor’s Degree'),
                'class': 'form-control',
            }
        ),
        required=False,
    )
    employment_status = forms.CharField(
        label=_('Employment Status'),
        widget=forms.TextInput(
            attrs={
                'placeholder': _('Employed'),
                'class': 'form-control',
            }
        ),
        required=False,
    )
    kyc_status = forms.BooleanField(
        label=_('KYC Status'),
        widget=forms.CheckboxInput(
            attrs={
                'class': 'form-control',
            }
        ),
        initial=True,
        required=False,
    )
    last_ok_date = forms.DateTimeField(
        label=_('Last OK Date'),
        input_formats=[settings.API_DATE_FORMAT_WITH_SECONDS ],
        widget=forms.DateTimeInput(
            attrs={
                'placeholder': PLACEHOLDER,
                'class': 'form-control',
            }
        ),
        required=True,
    )

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super(CreateCustomerForm, self).__init__(*args, **kwargs)

    def clean_face_image_date(self):
        data = self.cleaned_data['face_image_date']
        if data:
            return data.strftime(settings.API_DATE_FORMAT_WITH_SECONDS )
        else:
            return None

    def clean_dob_of_dependants(self):
        data = self.cleaned_data['dob_of_dependants']
        if data:
            return data.split(',')
        else:
            return []

    def clean_username(self):
        self.cleaned_data['user_id'] = self.cleaned_data["user_id"]
        user_id = self.cleaned_data['user_id']
        return user_id
