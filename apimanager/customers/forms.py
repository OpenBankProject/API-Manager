# -*- coding: utf-8 -*-
"""
Forms of customers app
"""

from django import forms

DATETIME_INPUT_FORMAT = '%Y-%m-%dT%H:%M:%SZ'


class CreateCustomerForm(forms.Form):
    bank_id = forms.ChoiceField(
        label='Bank',
        widget=forms.Select(
            attrs={
                'class': 'form-control',
            }
        ),
        choices=[],
    )
    user_id = forms.ChoiceField(
        label='User',
        widget=forms.Select(
            attrs={
                'class': 'form-control',
            }
        ),
        choices=[],
    )
    customer_number = forms.CharField(
        label='Customer Number',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'new customer number, e.g. 687687678',
                'class': 'form-control',
            }
        ),
    )
    legal_name = forms.CharField(
        label='Legal Name',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'NONE',
                'class': 'form-control',
            }
        ),
        required=False,
    )
    mobile_phone_number = forms.CharField(
        label='Mobile Phone Number',
        widget=forms.TextInput(
            attrs={
                'placeholder': '+49 123 456 78 90 12',
                'class': 'form-control',
            }
        ),
        required=False,
    )
    email = forms.CharField(
        label='Email',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'person@example.com',
                'class': 'form-control',
            }
        ),
        required=False,
    )
    face_image_url = forms.CharField(
        label='Face Image URL',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'https://static.openbankproject.com/images/OBP/favicon.png',
                'class': 'form-control',
            }
        ),
        required=False,
    )
    face_image_date = forms.DateTimeField(
        label='Face Image Date',
        input_formats=[DATETIME_INPUT_FORMAT],
        widget=forms.DateTimeInput(
            attrs={
                'placeholder': '2013-01-22T00:08:00Z',
                'class': 'form-control',
            }
        ),
        required=True,
    )
    date_of_birth = forms.DateTimeField(
        label='Date of Birth',
        input_formats=[DATETIME_INPUT_FORMAT],
        widget=forms.DateTimeInput(
            attrs={
                'placeholder': '2013-01-22T00:08:00Z',
                'class': 'form-control',
            }
        ),
        required=True,
    )
    relationship_status = forms.CharField(
        label='Relationship Status',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Single',
                'class': 'form-control',
            }
        ),
        required=False,
    )
    dependants = forms.IntegerField(
        label='Dependants',
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
        label='Date of Birth of Dependants',
        widget=forms.TextInput(
            attrs={
                'placeholder': '2013-01-22T00:08:00Z, 2010-01-22T00:08:00Z',
                'class': 'form-control',
            }
        ),
        required=False,
    )
    credit_rating_rating = forms.CharField(
        label='Credit Rating (Rating)',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'OBP',
                'class': 'form-control',
            }
        ),
        required=False,
    )
    credit_rating_source = forms.CharField(
        label='Credit Rating (Source)',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'OBP',
                'class': 'form-control',
            }
        ),
        required=False,
    )
    credit_limit_currency = forms.CharField(
        label='Credit Limit (Currency)',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'EUR',
                'class': 'form-control',
            }
        ),
        required=False,
    )
    credit_limit_amount = forms.CharField(
        label='Credit Limit (Amount)',
        widget=forms.TextInput(
            attrs={
                'placeholder': '10',
                'class': 'form-control',
            }
        ),
        required=False,
    )
    highest_education_attained = forms.CharField(
        label='Highest Education Attained',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Bachelor’s Degree',
                'class': 'form-control',
            }
        ),
        required=False,
    )
    employment_status = forms.CharField(
        label='Employment Status',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Employed',
                'class': 'form-control',
            }
        ),
        required=False,
    )
    kyc_status = forms.BooleanField(
        label='KYC Status',
        widget=forms.CheckboxInput(
            attrs={
                'class': 'form-control',
            }
        ),
        initial=True,
        required=False,
    )
    last_ok_date = forms.DateTimeField(
        label='Last OK Date',
        input_formats=[DATETIME_INPUT_FORMAT],
        widget=forms.DateTimeInput(
            attrs={
                'placeholder': '2013-01-22T00:08:00Z',
                'class': 'form-control',
            }
        ),
        required=True,
    )

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super(CreateCustomerForm, self).__init__(*args, **kwargs)
