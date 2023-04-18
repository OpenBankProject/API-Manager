"""
Forms of Accounts app
"""

from django import forms
from django.utils.translation import ugettext_lazy as _

import random


class CreateAccountForm(forms.Form):

    user_id = forms.CharField(
        label=_('User Id'),
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        ),
        required=True
    )
    bank_id = forms.ChoiceField(
        label=_('Bank Id'),
        widget=forms.Select(
            attrs={
                'class': 'form-control',
            }
        ),
        choices=[],
    )

    label = forms.CharField(
        label=_('Label'),
        widget=forms.TextInput(
            attrs={
                'placeholder': _('Select The Label'),
                'class': 'form-control',
            }
        ),
        required=False
    )

    product_code = forms.CharField(
        label=_('Product Code'),
        widget=forms.TextInput(
            attrs={
                'placeholder': "1234BW",
                'class': 'form-control',
            }
        ),
        required=False
    )

    balance_currency = forms.CharField(
        label=_('Currency'),
        widget=forms.TextInput(
            attrs={
                'placeholder': "EUR",
                'class': 'form-control',
            }
        ),
        required=True,
    )

    balance_amount = forms.FloatField(
        label=_('Amount'),
        widget=forms.TextInput(
            attrs={
                'placeholder': "0",
                'class': 'form-control',
            }
        ),
        required=False,
    )

    branch_id = forms.CharField(
        label=_('Branch Id'),
        widget=forms.TextInput(
            attrs={
                'placeholder': 'DERBY6',
                'class': 'form-control',
            }
        ),
        required=False,
    )

    account_routings_scheme = forms.CharField(
        label=_('Account Routing Scheme'),
        widget=forms.TextInput(
            attrs={
                'placeholder': _('IBAN'),
                'class': 'form-control',
            }
        ),
        required=False,
    )

    account_routings_address = forms.CharField(
        label=_('Account Routing Address'),
        widget=forms.TextInput(
            attrs={
                'placeholder': _('DE2100100100006820101'),
                'class': 'form-control',
            }
        ),
        required=False,
    )


    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super(CreateAccountForm, self).__init__(*args, **kwargs)
