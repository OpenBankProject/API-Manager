# -*- coding: utf-8 -*-
"""
Forms of consumers app
"""

from django import forms

class ApiConsumersForm(forms.Form):

    consumer_id = forms.CharField(
        widget=forms.HiddenInput(),
        required=True,
    )

    from_date = forms.DateTimeField(
        label='From Date',
        widget=forms.DateTimeInput(
            attrs={
                'class': 'form-control',
                'type': 'datetime-local',
                'value': '2024-01-01T00:00',
            }
        ),
        required=False,
        initial='2024-01-01T00:00:00',
    )

    to_date = forms.DateTimeField(
        label='To Date',
        widget=forms.DateTimeInput(
            attrs={
                'class': 'form-control',
                'type': 'datetime-local',
                'value': '2026-01-01T00:00',
            }
        ),
        required=False,
        initial='2026-01-01T00:00:00',
    )

    per_second_call_limit = forms.IntegerField(
        label='Per Second Call Limit',
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
            }
        ),
        initial=-1,
        required=False,
    )

    per_minute_call_limit = forms.IntegerField(
        label='Per Minute Call Limit',
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
            }
        ),
        initial=-1,
        required=False,
    )

    per_hour_call_limit = forms.IntegerField(
        label='Per Hour Call Limit',
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
            }
        ),
        initial=-1,
        required=False,
    )

    per_day_call_limit = forms.IntegerField(
        label='Per Day Call Limit',
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
            }
        ),
        initial=-1,
        required=False,
    )

    per_week_call_limit = forms.IntegerField(
        label='Per Week Call Limit',
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
            }
        ),
        initial=-1,
        required=False,
    )

    per_month_call_limit = forms.IntegerField(
        label='Per Month Call Limit',
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
            }
        ),
        initial=-1,
        required=False,
    )
