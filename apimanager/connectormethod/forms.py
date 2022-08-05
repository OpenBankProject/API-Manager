"""
Forms of ATMs app
"""

from django import forms
from django.utils.translation import ugettext_lazy as _
import random

class ConnectorMethodForm(forms.Form):
    api_collections_body = forms.CharField(
        label='API Collections Body',
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
            }
        ),
        required=False
    )

class ConnectorMethodEndpointForm(forms.Form):
    operation_id = forms.CharField(
        label='Operation Id',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        ),
        required=True
    )
class CreateConnectorMethodForm(forms.Form):
    connector_method_id = forms.CharField(
        label=_('Connector Method Id'),
        widget=forms.TextInput(
            attrs={
                'placeholder': 'connector_method_id-{}'.format(random.randint(1,1000)),
                'class': 'form-control',
            }
        ),
        initial='connector_method_id-{}'.format(random.randint(1,1000)),
    )
    method_name = forms.CharField(
        label=_('Method Name'),
        widget=forms.TextInput(
            attrs={
                'placeholder': _('Method Name'),
                'class': 'form-control',
            }
        ),
        required=True
    )
    programming_lang = forms.CharField(
        label=_('Programming Language'),
        widget=forms.TextInput(
            attrs={
                'placeholder': _('Programming Lang'),
                'class': 'form-control',
            }
        ),
        required=True
    )
    method_body = forms.CharField(
        label=_('Method Body'),
        widget=forms.TextInput(
            attrs={
                'placeholder': _('Method Body'),
                'class': 'form-control',
            }
        ),
        required=True
    )