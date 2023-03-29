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
from apimanager.settings import API_DATE_FORMAT_WITH_DAY, API_DATE_FORMAT_WITH_MILLISECONDS
from apimanager.settings import API_DATE_FORMAT_WITH_DAY, API_FIELD_TIME_FORMAT

API_DATE_FORMAT_WITH_MILLISECONDS_PLACEHOLDER = "yyyy-MM-dd'T'HH:mm:ss.SSS'Z'"
FORM_CONTROL = 'form-control'
FROM_DATE = 'From Date'
TO_DATE = 'To Date'
PLACEHOLDER = "2013-01-22"
PLACEHOLDER1 = "23:59:59"
PLACEHOLDER2 = "00:00:00"

class MetricsForm(forms.Form):
    from_date = forms.DateTimeField(
        label=_(FROM_DATE),
        input_formats=[settings.API_DATE_FORMAT_WITH_MILLISECONDS],
        widget=forms.DateTimeInput(
            attrs={
                'placeholder': API_DATE_FORMAT_WITH_MILLISECONDS,
                'class': FORM_CONTROL,
            }
        ),
        initial=(datetime.now() - timedelta(30)).strftime(settings.API_DATE_FORMAT_WITH_MILLISECONDS),
        required=False,
    )
    to_date = forms.DateTimeField(
        label=_(TO_DATE),
        input_formats=[settings.API_DATE_FORMAT_WITH_MILLISECONDS],
        widget=forms.DateTimeInput(
            attrs={
                'placeholder': API_DATE_FORMAT_WITH_MILLISECONDS,
                'class': FORM_CONTROL,
            }
        ),
        initial=str(datetime.now().strftime(settings.API_DATE_FORMAT_WITH_MILLISECONDS)),
        required=False,
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
        widget=DatePickerInput(format=API_DATE_FORMAT_WITH_DAY),
        required=True,
        initial=(datetime.now() - timedelta(6)).strftime(API_DATE_FORMAT_WITH_DAY),
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
        label=_("Date"),
        widget=DatePickerInput(format=API_DATE_FORMAT_WITH_DAY),
        required=True,
        initial=str(datetime.now().strftime(API_DATE_FORMAT_WITH_DAY)),
    )
    to_date_time = forms.TimeField(
        label=_('Time'),
        widget=forms.TimeInput(
            format='%H:%M:%S',
            attrs={
                'placeholder': PLACEHOLDER2,
                'class': 'form-control',
            }
        ),
        required=False,
    )
    from_date_custom = forms.DateField(
        label=_(FROM_DATE),
        widget=DatePickerInput(format=API_DATE_FORMAT_WITH_DAY),
        required=True,
        initial=(datetime.now() - timedelta(6)).strftime(API_DATE_FORMAT_WITH_DAY),
    )
    from_time_custom = forms.TimeField(
        label=_('Time'),
        widget=forms.TimeInput(
            format='%H:%M:%S',
            attrs={
                'placeholder': PLACEHOLDER1,
                'class': 'form-control',
            }
        ),
        required=False,
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
    to_date = forms.DateField(
        label=_("Date"),
        widget=DatePickerInput(format=API_DATE_FORMAT_WITH_DAY),
        required=True,
        initial=str(datetime.now().strftime(API_DATE_FORMAT_WITH_DAY)),
    )
    to_date_time = forms.TimeField(
        label=_('Time'),
        widget=forms.TimeInput(
            format='%H:%M:%S',
            attrs={
                'placeholder': PLACEHOLDER1,
                'class': 'form-control',
            }
        ),
        required=False,
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