# -*- coding: utf-8 -*-
"""
Forms of metrics app
"""

from django import forms
from django.conf import settings
from datetime import date
from django.forms.widgets import SelectMultiple, CheckboxInput, CheckboxSelectMultiple
from datetime import datetime, timedelta
from django.utils.translation import ugettext_lazy as _

from bootstrap_datepicker_plus import DatePickerInput, DateTimePickerInput
from apimanager.settings import API_MANAGER_DATE_FORMAT

API_DATE_FORMAT_PLACEHOLDER = "yyyy-MM-dd'T'HH:mm:ss.SSS'Z'"
FORM_CONTROL = 'form-control'
FROM_DATE = 'From Date'
TO_DATE = 'To Date'

class MetricsForm(forms.Form):
    from_date = forms.DateTimeField(
       label=_(FROM_DATE),
       widget=DatePickerInput(format=API_MANAGER_DATE_FORMAT),
       required=False,
       initial=(datetime.now() - timedelta(6)).strftime(API_MANAGER_DATE_FORMAT),
    )
    to_date = forms.DateTimeField(
        label=_(TO_DATE),
        widget=DatePickerInput(format=API_MANAGER_DATE_FORMAT),
        required=False,
        initial=str(datetime.now().strftime(API_MANAGER_DATE_FORMAT)),
    )
    limit = forms.IntegerField(
        label=_('Limit'),
        widget=forms.NumberInput(
            attrs={
                'class': FORM_CONTROL,
            }
        ),
        initial=100,
        required=False,
    )
    offset = forms.IntegerField(
        label=_('Offset'),
        widget=forms.NumberInput(
            attrs={
                'class': FORM_CONTROL,
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
        ('', _('Anonymous and Non-Anonymous')),
        ('true', 'Yes'),
        ('false', 'No'),
    )
    VERB = (
        ('', _('Any')),
        ('DELETE', 'DELETE'),
        ('GET', 'GET'),
        ('POST', 'POST'),
        ('PUT', 'PUT'),
    )
    VERSION = (
        ('', _('Any')),
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
        label=_('Consumer ID'),
        widget=forms.TextInput(
            attrs={
                'class': FORM_CONTROL,
            }
        ),
        required=False,
    )
    user_id = forms.CharField(
        label=_('User ID'),
        widget=forms.TextInput(
            attrs={
                'class': FORM_CONTROL,
            }
        ),
        required=False,
    )
    anon = forms.ChoiceField(
        label=_('Anonymous'),
        choices=ANONYMOUS,
        widget=forms.Select(
            attrs={
                'class': FORM_CONTROL,
            }
        ),
        initial='',
        required=False,
    )
    app_name = forms.CharField(
        label=_('App Name'),
        widget=forms.TextInput(
            attrs={
                'class': FORM_CONTROL,
            }
        ),
        required=False,
    )
    verb = forms.ChoiceField(
        label=_('Verb'),
        choices=VERB,
        widget=forms.Select(
            attrs={
                'class': FORM_CONTROL,
            }
        ),
        initial='',
        required=False,
    )
    url = forms.CharField(
        label=_('URL'),
        widget=forms.TextInput(
            attrs={
                'class': FORM_CONTROL,
            }
        ),
        required=False,
    )
    implemented_by_partial_function = forms.CharField(
        label=_('Implemented By Partial Function'),
        widget=forms.TextInput(
            attrs={
                'class': FORM_CONTROL,
            }
        ),
        required=False,
    )
    implemented_in_version = forms.ChoiceField(
        label=_('Implemented In Version'),
        choices=VERSION,
        widget=forms.Select(
            attrs={
                'class': FORM_CONTROL,
            }
        ),
        initial='',
        required=False,
    )


class ConnectorMetricsForm(MetricsForm):
    # override from_date until API returns values without given date
    from_date = forms.DateTimeField(
        label=_(FROM_DATE),
        widget=DatePickerInput(format=API_MANAGER_DATE_FORMAT),
        required=True,
        initial=(datetime.now() - timedelta(6)).strftime(API_MANAGER_DATE_FORMAT),
    )
    connector_name = forms.CharField(
        label=_('Connector Name'),
        widget=forms.TextInput(
            attrs={
                'class': FORM_CONTROL,
            }
        ),
        required=False,
    )
    function_name = forms.CharField(
        label=_('Function Name'),
        widget=forms.TextInput(
            attrs={
                'class': FORM_CONTROL,
            }
        ),
        required=False,
    )
    correlation_id = forms.CharField(
        label=_('Correlation ID'),
        widget=forms.TextInput(
            attrs={
                'class': FORM_CONTROL,
            }
        ),
        required=False,
    )


class CustomSummaryForm(forms.Form):
    to_date = forms.DateField(
        label=_(TO_DATE),
        widget=DatePickerInput(format=API_MANAGER_DATE_FORMAT),
        required=True,
        initial=str(datetime.now().strftime(API_MANAGER_DATE_FORMAT)),
    )

    from_date_custom = forms.DateField(
        label=_(FROM_DATE),
        widget=DatePickerInput(format=API_MANAGER_DATE_FORMAT),
        required=True,
        initial=(datetime.now() - timedelta(6)).strftime(API_MANAGER_DATE_FORMAT),
    )
    exclude_app_names = forms.CharField(
        label=_('Exclude App Names'),
        widget=forms.TextInput(
            attrs={
                'class': FORM_CONTROL,
            }
        ),
        required=False,
        initial='API-Manager',
    )
    include_obp_apps = forms.BooleanField(required=False, label=_('Include System Data'))

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super(CustomSummaryForm, self).__init__(*args, **kwargs)

class MonthlyMetricsSummaryForm(forms.Form):
    to_date = forms.DateField(
        label=_(TO_DATE),
        widget=DatePickerInput(format=API_MANAGER_DATE_FORMAT),
        required=True,
        #initial=str(datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%fZ')),
        initial=str(datetime.now().strftime(API_MANAGER_DATE_FORMAT)),
    )
    exclude_app_names = forms.CharField(
        label=_('Exclude App Names'),
        widget=forms.TextInput(
            attrs={
                'class': FORM_CONTROL,
            }
        ),
        required=False,
        initial='API-Manager',
    )
    include_obp_apps = forms.BooleanField(required=False, label=_('Include System Data'))

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super(MonthlyMetricsSummaryForm, self).__init__(*args, **kwargs)