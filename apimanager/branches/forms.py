"""
Forms of branches app
"""

from django import forms

import random


class CreateBranchForm(forms.Form):

    branch_id = forms.CharField(
        label='Branch Id',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'branch-id-{}'.format(random.randint(1,1000)),
                'class': 'form-control',
            }
        ),
        initial='branch-id-{}'.format(random.randint(1,1000)),
    )

    bank_id = forms.ChoiceField(
        label='Bank',
        widget=forms.Select(
            attrs={
                'class': 'form-control',
            }
        ),
        choices=[],
    )
    name = forms.CharField(
        label='Name',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'The name of the branch',
                'class': 'form-control',
            }
        ),
        required=True
    )
    address_line1 = forms.CharField(
        label='address_line1',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'No 1 the Road',
                'class': 'form-control',
            }
        ),
        required=False
    )

    address_line2 = forms.CharField(
        label='address_line2',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'The Place',
                'class': 'form-control',
            }
        ),
        required=False
    )

    address_line3 = forms.CharField(
        label='address_line3',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'The Hill',
                'class': 'form-control',
            }
        ),
        required=False
    )

    address_city = forms.CharField(
        label='city',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Berlin',
                'class': 'form-control',
            }
        ),
        required=False
    )

    address_county = forms.CharField(
        label='county',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'String',
                'class': 'form-control',
            }
        ),
        required=False
    )

    address_state = forms.CharField(
        label='state',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Brandenburg',
                'class': 'form-control',
            }
        ),
        required=False
    )

    address_postcode = forms.CharField(
        label='state',
        widget=forms.TextInput(
            attrs={
                'placeholder': '13359',
                'class': 'form-control',
            }
        ),
        required=False
    )

    address_country_code = forms.CharField(
        label='country_code',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'DE',
                'class': 'form-control',
            }
        ),
        required=False
    )

    location_latitude = forms.FloatField(
        label='Latitude',
        widget=forms.TextInput(
            attrs={
                'placeholder': 37.0,
                'class': 'form-control',
            }
        ),
        required=False,
    )

    location_longitude = forms.FloatField(
        label='Longitude',
        widget=forms.TextInput(
            attrs={
                'placeholder': 110.0,
                'class': 'form-control',
            }
        ),
        required=False,
    )

    meta_license_id = forms.CharField(
        label='meta_license_id',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'PDDL',
                'class': 'form-control',
            }
        ),
        required=False,
    )

    meta_license_name = forms.CharField(
        label='meta_license_name',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Open Data Commons Public Domain Dedication and License',
                'class': 'form-control',
            }
        ),
        required=False,
    )

    lobby = forms.CharField(
        label='Lobby',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'None',
                'class': 'form-control',
            }
        ),
        required=False,
    )
    drive_up = forms.CharField(
        label='Drive Up',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'None',  # noqa
                'class': 'form-control',
            }
        ),
        required=False,
    )
    branch_routing_scheme = forms.CharField(
        label='Branch Routing Scheme',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'OBP',
                'class': 'form-control',
            }
        ),
        required=False,
    )
    branch_routing_address = forms.CharField(
        label='Branch Routing Address',
        widget=forms.TextInput(
            attrs={
                'placeholder': '123abc',
                'class': 'form-control',
            }
        ),
        required=False,
    )
    is_accessible = forms.CharField(
        label='is accessible',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'true',
                'class': 'form-control',
            }
        ),
        required=False,
    )
    accessibleFeatures = forms.CharField(
        label='Accessible Features',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'wheelchair, atm usuable by the visually impaired',
                'class': 'form-control',
            }
        ),
        required=False,
    )
    branch_type = forms.CharField(
        label='Branch type',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Full service store',
                'class': 'form-control',
            }
        ),
        required=False,
    )
    more_info = forms.CharField(
        label='More information',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'short walk to the lake from here',
                'class': 'form-control',
            }
        ),
        required=False,
    )

    phone_number = forms.CharField(
        label='Mobile Phone Number',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'E.g. +49 123 456 78 90 12',
                'class': 'form-control',
            }
        ),
        required=False,
    )

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super(CreateBranchForm, self).__init__(*args, **kwargs)
