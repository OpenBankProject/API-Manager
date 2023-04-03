"""
Forms of Banks app
"""

from django import forms
from django.utils.translation import ugettext_lazy as _

import random


class CreateBankForm(forms.Form):

    bank_id = forms.CharField(
        label=_('Bank Id'),
        widget=forms.TextInput(
            attrs={
                'placeholder': 'bank-id-{}'.format(random.randint(1,1000)),
                'class': 'form-control',
            }
        ),
        initial='bank-id-{}'.format(random.randint(1,1000)),
    )

    bank_code = forms.CharField(
        label=_('Bank Code'),
        widget=forms.TextInput(
            attrs={
                'placeholder': _('CGHZ'),
                'class': 'form-control',
            }
        ),
        required=False
    )

    full_name = forms.CharField(
        label=_('Full Name'),
        widget=forms.TextInput(
            attrs={
                'placeholder': "full name string",
                'class': 'form-control',
            }
        ),
        required=False
    )

    logo = forms.CharField(
        label=_('Logo URL'),
        widget=forms.TextInput(
            attrs={
                'placeholder': "logo url",
                'class': 'form-control',
            }
        ),
        required=False,
    )

    website = forms.CharField(
        label=_('Website'),
        widget=forms.TextInput(
            attrs={
                'placeholder': "www.openbankproject.com",
                'class': 'form-control',
            }
        ),
        required=False,
    )

    bank_routings_scheme = forms.CharField(
        label=_('Bank Routing Scheme'),
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Scheme Value',
                'class': 'form-control',
            }
        ),
        required=False,
    )

    bank_routings_address = forms.CharField(
        label=_('Bank Routing Address'),
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Bank Routing Address',
                'class': 'form-control',
            }
        ),
        required=False,
    )

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super(CreateBankForm, self).__init__(*args, **kwargs)
