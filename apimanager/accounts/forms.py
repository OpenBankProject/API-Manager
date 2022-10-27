"""
Forms of Accounts app
"""

from django import forms
from django.utils.translation import ugettext_lazy as _

import random


class CreateAccountForm(forms.Form):

    account_id = forms.CharField(
        label=_('Account Id'),
        widget=forms.TextInput(
            attrs={
                'placeholder': 'account-id-{}'.format(random.randint(1,1000)),
                'class': 'form-control',
            }
        ),
        initial='account-id-{}'.format(random.randint(1,1000)),
    )

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
                'placeholder': _('Select the label'),
                'class': 'form-control',
            }
        ),
        required=False
    )

    product_code = forms.CharField(
        label=_('Write Product Code'),
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
        label=_('Account Number'),
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Account Number',
                'class': 'form-control',
            }
        ),
        required=False,
    )

    account_routings_address = forms.CharField(
        label=_('Address'),
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Address',
                'class': 'form-control',
            }
        ),
        required=False,
    )
    account_attributes_product_code = forms.CharField(
           label=_('Account Attribute Product Code'),
           widget=forms.TextInput(
               attrs={
                   'placeholder': '1234BW',
                   'class': 'form-control',
               }
           ),
           required=False,
       )
    account_attributes_id = forms.CharField(
           label=_('Account Attribute Id'),
           widget=forms.TextInput(
               attrs={
                   'placeholder': '613c83ea-80f9-4560-8404-b9cd4ec42a7f',
                   'class': 'form-control',
               }
           ),
           required=False,
       )
    account_attributes_name = forms.CharField(
           label=_('Account Attribute Name'),
           widget=forms.TextInput(
               attrs={
                   'placeholder': 'OVERDRAFT_START_DATE',
                   'class': 'form-control',
               }
           ),
           required=False,
       )
    account_attributes_value = forms.CharField(
           label=_('Thursday'),
           widget=forms.TextInput(
               attrs={
                   'placeholder': '2012-04-23',
                   'class': 'form-control',
               }
           ),
           required=False,
       )
    account_attributes_instance_code = forms.CharField(
           label=_('Account Attribute Instance Code'),
           widget=forms.TextInput(
               attrs={
                   'placeholder': 'LKJL98769F',
                   'class': 'form-control',
               }
           ),
           required=False,
       )

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super(CreateAccountForm, self).__init__(*args, **kwargs)
