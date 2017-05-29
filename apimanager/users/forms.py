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
