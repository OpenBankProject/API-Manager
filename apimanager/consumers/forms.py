# -*- coding: utf-8 -*-
"""
Forms of consumers app
"""

from django import forms



class ApiConsumersForm(forms.Form):

    consumer_id = forms.CharField(
        label='Consumer ID',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        ),
        required=False,
    )

    per_minute_call_limit = forms.IntegerField(
        label='per_minute_call_limit',
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
            }
        ),
        required=False,
    )

    per_hour_call_limit = forms.IntegerField(
        label='per_hour_call_limit',
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
            }
        ),
        required=False,
    )
    per_day_call_limit = forms.IntegerField(
        label='per_day_call_limit',
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
            }
        ),
        required=False,
    )
    per_week_call_limit = forms.IntegerField(
        label='per_week_call_limit',
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
            }
        ),
        required=False,
    )

    per_month_call_limit = forms.IntegerField(
        label='per_month_call_limit',
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
            }
        ),
        required=False,
    )
