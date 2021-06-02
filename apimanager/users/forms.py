# -*- coding: utf-8 -*-
"""
Forms of users app
"""

from django import forms

class AddEntitlementForm(forms.Form):
    user_id = forms.CharField(
        widget=forms.HiddenInput(),
        required=True,
    )
    role_name = forms.CharField(
        label='Role name',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        ),
        required=True,
    )
    bank_id = forms.ChoiceField(
        label='Bank',
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
        label='Bank',
        widget=forms.Select(
            attrs={
                'class': 'form-control',
            }
        ),
        choices=[],
    )
    first_name = forms.CharField(
        label='First Name',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'First Name',
                'class': 'form-control',
            }
        ),
    )
    last_name = forms.CharField(
        label='Last Name',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Last Name',
                'class': 'form-control',
            }
        ),
    )
    email = forms.CharField(
        label='Email',
        widget=forms.EmailInput(
            attrs={
                'placeholder': 'felixsmith@example.com',
                'class': 'form-control',
            }
        ),
        required=False,
    )
    company = forms.CharField(
        label='Company',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'TESOBE GmbH',
                'class': 'form-control',
            }
        ),
        required=False,
    )
    country = forms.CharField(
        label='Country',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Germany',
                'class': 'form-control',
            }
        ),
        required=False,
    )
    purpose = forms.CharField(
        label='Purpose',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'For the Bank App',
                'class': 'form-control',
            }
        ),
        required=False,
    )

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super(CreateInvitationForm, self).__init__(*args, **kwargs)
