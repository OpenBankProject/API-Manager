# -*- coding: utf-8 -*-
"""
Forms of users app
"""

from django import forms
from django.utils.translation import ugettext_lazy as _

class AddEntitlementForm(forms.Form):
    user_id = forms.CharField(
        widget=forms.HiddenInput(),
        required=True,
    )
    role_name = forms.CharField(
        label=_('Role name'),
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        ),
        required=True,
    )
    bank_id = forms.ChoiceField(
        label=_('Bank'),
        widget=forms.Select(
            attrs={
                'class': 'form-control',
            }
        ),
        choices=[],
        required=False,
    )

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super(AddEntitlementForm, self).__init__(*args, **kwargs)

class CreateInvitationForm(forms.Form):
    bank_id = forms.ChoiceField(
        label=_('Bank'),
        widget=forms.Select(
            attrs={
                'class': 'form-control',
            }
        ),
        choices=[],
    )
    first_name = forms.CharField(
        label=_('First Name'),
        widget=forms.TextInput(
            attrs={
                'placeholder': _('First Name'),
                'class': 'form-control',
            }
        ),
    )
    last_name = forms.CharField(
        label=_('Last Name'),
        widget=forms.TextInput(
            attrs={
                'placeholder': _('Last Name'),
                'class': 'form-control',
            }
        ),
    )
    email = forms.CharField(
        label=_('Email'),
        widget=forms.EmailInput(
            attrs={
                'placeholder': 'felixsmith@example.com',
                'class': 'form-control',
            }
        ),
        required=True,
    )
    company = forms.CharField(
        label=_('Company'),
        widget=forms.TextInput(
            attrs={
                'placeholder': _('TESOBE GmbH'),
                'class': 'form-control',
            }
        ),
        required=True,
    )
    country = forms.CharField(
        label=_('Country'),
        widget=forms.TextInput(
            attrs={
                'placeholder': _('Germany'),
                'class': 'form-control',
            }
        ),
        required=True,
    )
    purpose = forms.CharField(
        label=_('Purpose'),
        widget=forms.TextInput(
            attrs={
                'placeholder': _('For the Bank App'),
                'class': 'form-control',
            }
        ),
        required=False,
    )

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super(CreateInvitationForm, self).__init__(*args, **kwargs)
