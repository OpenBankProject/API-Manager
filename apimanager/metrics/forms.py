# -*- coding: utf-8 -*-
"""
Forms of metrics app
"""

from django import forms
from django.conf import settings


class MetricsForm(forms.Form):
    start_date = forms.DateTimeField(
        label='Start Date',
        input_formats=[settings.API_DATEFORMAT],
        widget=forms.DateTimeInput(
            attrs={
                'placeholder': 'yyyy-mm-dd',
                'class': 'form-control',
            }
        ),
        required=False,
    )
    end_date = forms.DateTimeField(
        label='End Date',
        input_formats=[settings.API_DATEFORMAT],
        widget=forms.DateTimeInput(
            attrs={
                'placeholder': 'yyyy-mm-dd',
                'class': 'form-control',
            }
        ),
        required=False,
    )
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
        super(MetricsForm, self).__init__(*args, **kwargs)


class APIMetricsForm(MetricsForm):
    ANONYMOUS = (
        ('', 'Anonymous and Non-Anonymous'),
        ('true', 'Yes'),
        ('false', 'No'),
    )
    VERB = (
        ('', 'Any'),
        ('DELETE', 'DELETE'),
        ('GET', 'GET'),
        ('POST', 'POST'),
        ('PUT', 'PUT'),
    )
    VERSION = (
        ('', 'Any'),
        ('v1.2', '1.2'),
        ('v1.2.1', '1.2.1'),
        ('v1.3.0', '1.3.0'),
        ('v1.4.0', '1.4.0'),
        ('v2.0.0', '2.0.0'),
        ('v2.1.0', '2.1.0'),
        ('v2.2.0', '2.2.0'),
        ('v3.0.0', '3.0.0'),
    )

    consumer_id = forms.CharField(
        label='Consumer ID',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        ),
        required=False,
    )
    user_id = forms.CharField(
        label='User ID',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        ),
        required=False,
    )
    anon = forms.ChoiceField(
        label='Anonymous',
        choices=ANONYMOUS,
        widget=forms.Select(
            attrs={
                'class': 'form-control',
            }
        ),
        initial='',
        required=False,
    )
    app_name = forms.CharField(
        label='App Name',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        ),
        required=False,
    )
    verb = forms.ChoiceField(
        label='Verb',
        choices=VERB,
        widget=forms.Select(
            attrs={
                'class': 'form-control',
            }
        ),
        initial='',
        required=False,
    )
    url = forms.CharField(
        label='URL',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        ),
        required=False,
    )
    implemented_by_partial_function = forms.CharField(
        label='Implemented By Partial Function',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        ),
        required=False,
    )
    implemented_in_version = forms.ChoiceField(
        label='Implemented In Version',
        choices=VERSION,
        widget=forms.Select(
            attrs={
                'class': 'form-control',
            }
        ),
        initial='',
        required=False,
    )


class ConnectorMetricsForm(MetricsForm):
    # override start_date until API returns values without given date
    start_date = forms.DateTimeField(
        label='Start Date',
        input_formats=[settings.API_DATEFORMAT],
        widget=forms.DateTimeInput(
            attrs={
                'placeholder': 'yyyy-mm-dd',
                'class': 'form-control',
            }
        ),
        initial='1970-01-01',
        required=True,
    )
    connector_name = forms.CharField(
        label='Connector Name',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        ),
        required=False,
    )
    function_name = forms.CharField(
        label='Function Name',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        ),
        required=False,
    )
    obp_api_request_id = forms.CharField(
        label='OBP API Request ID',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        ),
        required=False,
    )
