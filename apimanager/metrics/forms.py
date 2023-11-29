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

from bootstrap_datepicker_plus import DateTimePickerInput
from apimanager.settings import API_DATE_FORMAT_WITH_DAY_DATE_TIME

API_DATE_FORMAT_WITH_MILLISECONDS_PLACEHOLDER = "yyyy-MM-dd'T'HH:mm:ss.SSS'Z'"
FORM_CONTROL = 'form-control'
FROM_DATE = 'From Date Time'
TO_DATE = 'To Date Time'
PLACEHOLDER = "2013-01-22"
PLACEHOLDER1 = "2022-01-01 12:30:45"
PLACEHOLDER2 = "00:00:00"

class MetricsForm(forms.Form):
    from_date = forms.DateTimeField(
        label=_(FROM_DATE),
        widget=DateTimePickerInput(format=API_DATE_FORMAT_WITH_DAY_DATE_TIME),
        required=True,
        initial=(datetime.now() - timedelta(1)).strftime(API_DATE_FORMAT_WITH_DAY_DATE_TIME),
    )

    to_date = forms.DateTimeField(
        label=_(TO_DATE),
        widget=DateTimePickerInput(format=API_DATE_FORMAT_WITH_DAY_DATE_TIME),
        required=True,
        initial=(datetime.now() - timedelta()).strftime(API_DATE_FORMAT_WITH_DAY_DATE_TIME),
    )
  
    limit = forms.IntegerField(
        label=_('Limit'),
        widget=forms.NumberInput(
            attrs={
                'class': FORM_CONTROL,
            }
        ),
        initial=1000,
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

    consumer_id = forms.ChoiceField(
        label=_('Consumer ID'),
        widget=forms.Select(
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
        widget=forms.Select(
            attrs={
                'class': FORM_CONTROL,
            }
        ),
        choices=[],
        required=False,
    )

class ConnectorMetricsForm(MetricsForm):
    # override from_date until API returns values without given date
    from_date = forms.DateTimeField(
        label=_(FROM_DATE),
        widget=DateTimePickerInput(format=API_DATE_FORMAT_WITH_DAY_DATE_TIME),
        required=True,
        initial=(datetime.now() - timedelta(6)).strftime(API_DATE_FORMAT_WITH_DAY_DATE_TIME),
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
    to_date = forms.DateTimeField(
        label=_(TO_DATE),
        widget=DateTimePickerInput(format=API_DATE_FORMAT_WITH_DAY_DATE_TIME),
        required=True,
        initial=(datetime.now()).strftime(API_DATE_FORMAT_WITH_DAY_DATE_TIME),
    )
    from_date_custom = forms.DateTimeField(
        label=_(FROM_DATE),
        widget=DateTimePickerInput(format=API_DATE_FORMAT_WITH_DAY_DATE_TIME),
        required=True,
        initial=(datetime.now() - timedelta(6)).strftime(API_DATE_FORMAT_WITH_DAY_DATE_TIME),
    )
    include_app_names = forms.CharField(
        label=_('Include App Names'),
        widget=forms.TextInput(
            attrs={
                'class': FORM_CONTROL,
            }
        ),
        required=False,
    )


    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super(CustomSummaryForm, self).__init__(*args, **kwargs)

class MonthlyMetricsSummaryForm(forms.Form):
    to_date = forms.DateTimeField(
        label=_(TO_DATE),
        widget=DateTimePickerInput(format=API_DATE_FORMAT_WITH_DAY_DATE_TIME),
        required=True,
        initial=(datetime.now()).strftime(API_DATE_FORMAT_WITH_DAY_DATE_TIME),
    )
    include_app_names = forms.CharField(
        label=_('Include App Names'),
        widget=forms.TextInput(
            attrs={
                'class': FORM_CONTROL,
            }
        ),
        required=False,
    )

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super(MonthlyMetricsSummaryForm, self).__init__(*args, **kwargs)