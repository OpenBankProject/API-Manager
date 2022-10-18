"""
Forms of branches app
"""

from django import forms
from django.utils.translation import ugettext_lazy as _
import random


class CreateBranchForm(forms.Form):

    branch_id = forms.CharField(
        label=_('Branch Id'),
        widget=forms.TextInput(
            attrs={
                'placeholder': 'branch-id-{}'.format(random.randint(1,1000)),
                'class': 'form-control',
            }
        ),
        initial='branch-id-{}'.format(random.randint(1,1000)),
    )

    bank_id = forms.ChoiceField(
        label=_('Bank'),
        widget=forms.Select(
            attrs={
                'class': 'form-control',
            }
        ),
        choices=[],
    )
    view_id = forms.ChoiceField(
        label=_('View Id'),
        widget=forms.Select(
            attrs={
                'class': 'form-control',
            }
        ),
        choices=[],
    )
    name = forms.CharField(
        label=_('Name'),
        widget=forms.TextInput(
            attrs={
                'placeholder': _('The name of the branch'),
                'class': 'form-control',
            }
        ),
        required=True
    )
    address = forms.CharField(
        label=_('Address'),
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
            }
        ),
        required=False
    )

    location_latitude = forms.FloatField(
        label=_('Latitude'),
        widget=forms.TextInput(
            attrs={
                'placeholder': 37.0,
                'class': 'form-control',
            }
        ),
        required=False,
    )

    location_longitude = forms.FloatField(
        label=_('Longitude'),
        widget=forms.TextInput(
            attrs={
                'placeholder': 110.0,
                'class': 'form-control',
            }
        ),
        required=False,
    )

    meta_license_id = forms.CharField(
        label=_('meta_license_id'),
        widget=forms.TextInput(
            attrs={
                'placeholder': 'PDDL',
                'class': 'form-control',
            }
        ),
        required=False,
    )

    meta_license_name = forms.CharField(
        label=_('meta_license_name'),
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Open Data Commons Public Domain Dedication and License',
                'class': 'form-control',
            }
        ),
        required=False,
    )

    lobby = forms.CharField(
        label=_(' Lobby Opening Hours'),
        widget=forms.Textarea(
            attrs={
                'placeholder': 'None',
                'class': 'form-control',
            }
        ),
        required=False,
    )
    drive_up = forms.CharField(
        label=_('Drive Up'),
        widget=forms.Textarea(
            attrs={
                'placeholder': 'None',  # noqa
                'class': 'form-control',
            }
        ),
        required=False,
    )
    branch_routing_scheme = forms.CharField(
        label=_('Branch Routing Scheme'),
        widget=forms.TextInput(
            attrs={
                'placeholder': 'OBP',
                'class': 'form-control',
            }
        ),
        required=False,
    )
    branch_routing_address = forms.CharField(
        label=_('Branch Routing Address'),
        widget=forms.TextInput(
            attrs={
                'placeholder': '123abc',
                'class': 'form-control',
            }
        ),
        required=False,
    )
    is_accessible = forms.ChoiceField(
        label=_('is accessible'),
        widget=forms.Select(
            attrs={
                'class': 'form-control',
            }
        ),
        required=False,
    )
    accessibleFeatures = forms.CharField(
        label=_('Accessible Features'),
        widget=forms.TextInput(
            attrs={
                'placeholder': _('wheelchair, atm useable by the visually impaired'),
                'class': 'form-control',
            }
        ),
        required=False,
    )
    branch_type = forms.CharField(
        label=_('Branch type'),
        widget=forms.TextInput(
            attrs={
                'placeholder': _('Full service store'),
                'class': 'form-control',
            }
        ),
        required=False,
    )
    more_info = forms.CharField(
        label=_('More information'),
        widget=forms.TextInput(
            attrs={
                'placeholder': _('short walk to the lake from here'),
                'class': 'form-control',
            }
        ),
        required=False,
    )

    phone_number = forms.CharField(
        label=_('Mobile Phone Number'),
        widget=forms.TextInput(
            attrs={
                'placeholder': _('E.g. +49 123 456 78 90 12'),
                'class': 'form-control',
            }
        ),
        required=False,
    )

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super(CreateBranchForm, self).__init__(*args, **kwargs)
