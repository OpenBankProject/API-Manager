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

class UsersForm(forms.Form):
    limit = forms.IntegerField(
        label='Limit',
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
            }
        ),
        initial=100,
        required=False,
    )
    offset = forms.IntegerField(
        label='Offset',
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
            }
        ),
        initial=0,
        required=False,
    )

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super(UsersForm, self).__init__(*args, **kwargs)
