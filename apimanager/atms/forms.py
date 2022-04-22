"""
Forms of ATMs app
"""

from django import forms

import random


class CreateAtmForm(forms.Form):

    atm_id = forms.CharField(
        label='ATM Id',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'atm-id-{}'.format(random.randint(1,1000)),
                'class': 'form-control',
            }
        ),
        initial='atm-id-{}'.format(random.randint(1,1000)),
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
                'placeholder': 'The name of the ATM',
                'class': 'form-control',
            }
        ),
        required=True
    )

    address = forms.CharField(
        label='Address',
        widget=forms.Textarea(
            attrs={
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

    """ lobby = forms.CharField(
        label=' Lobby Opening Hours',
        widget=forms.Textarea(
            attrs={
                'placeholder': 'None',
                'class': 'form-control',
            }
        ),
        required=False,
    )"""
    monday = forms.CharField(
           label=' Monday',
           widget=forms.Textarea(
               attrs={
                   'placeholder': 'None',
                   'class': 'form-control',
               }
           ),
           required=False,
       )
    tuesday = forms.CharField(
           label='Tuesday',
           widget=forms.Textarea(
               attrs={
                   'placeholder': 'None',
                   'class': 'form-control',
               }
           ),
           required=False,
       )
    wednesday = forms.CharField(
           label=' Wednesday',
           widget=forms.Textarea(
               attrs={
                   'placeholder': 'None',
                   'class': 'form-control',
               }
           ),
           required=False,
       )
    thursday = forms.CharField(
           label=' Thursday',
           widget=forms.Textarea(
               attrs={
                   'placeholder': 'None',
                   'class': 'form-control',
               }
           ),
           required=False,
       )
    friday = forms.CharField(
           label=' Friday',
           widget=forms.Textarea(
               attrs={
                   'placeholder': 'None',
                   'class': 'form-control',
               }
           ),
           required=False,
       )
    saturday = forms.CharField(
           label=' Saturday',
           widget=forms.Textarea(
               attrs={
                   'placeholder': 'None',
                   'class': 'form-control',
               }
           ),
           required=False,
       )
    sunday = forms.CharField(
           label=' Sunday',
           widget=forms.Textarea(
               attrs={
                   'placeholder': 'None',
                   'class': 'form-control',
               }
           ),
           required=False,
       )
    located_at = forms.CharField(
        label='ATM location',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'OBP',
                'class': 'form-control',
            }
        ),
        required=False,
    )

    is_accessible = forms.ChoiceField(
        label='is accessible',
        widget=forms.Select(
            attrs={
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

    services = forms.CharField(
        label='Services',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Service store',
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

    supported_currencies = forms.ChoiceField(
        label='Supported Currencies',
        widget=forms.Select(
            attrs={
                'class': 'form-control',
            }
        ),
        required=False,
    )

    notes = forms.ChoiceField(
        label='Write Notes',
        widget=forms.Select(
            attrs={
               'class': 'form-control',
            }
        ),
        required=False,
    )

    location_categories = forms.ChoiceField(
        label='Write location Category',
        widget=forms.Select(
           attrs={
              'class': 'form-control',
           }
        ),
        required=False,
    )

    minimum_withdrawal = forms.CharField(
        label='Minimum Withdrawal',
        widget=forms.TextInput(
            attrs={
                'placeholder': '5',
                 'class': 'form-control',
            }
        ),
        required=False,
    )

    site_name = forms.CharField(
        label='Site Name',
        widget=forms.TextInput(
            attrs={
               'placeholder': 'Enter your Site Name ',
               'class': 'form-control',
            }
        ),
        required=False,
    )

    branch_identification = forms.CharField(
        label='Branch Identification',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Enter your Branch Identification',
                'class': 'form-control',
            }
        ),
        required=False,
    )

    site_identification = forms.CharField(
        label='Site Identification',
        widget=forms.TextInput(
            attrs={
               'placeholder': 'Enter your Site Identification',
               'class': 'form-control',
            }
        ),
        required=False,
    )

    services = forms.CharField(
        label='Services',
        widget=forms.TextInput(
             attrs={
                    'placeholder': 'Services Are',
                     'class': 'form-control',
             }
        ),
        required=False,
    )

    supported_languages = forms.ChoiceField(
        label='supported_languages',
        widget=forms.Select(
           attrs={
                  'class': 'form-control',
           }
        ),
        required=False,
    )

    has_deposit_capability = forms.ChoiceField(
         label='Deposit Capabilities',
         widget=forms.Select(
              attrs={
                     'class': 'form-control',
              }
         ),
         required=False,
    )

    cash_withdrawal_national_fee = forms.CharField(
         label='Cash Withdrawal National fee',
         widget=forms.TextInput(
              attrs={
                     'placeholder': 'Cash withdrawal national fee',
                     'class': 'form-control',
              }
         ),
         required=False,
    )

    cash_withdrawal_international_fee = forms.CharField(
         label='Cash Withdrawal international fee',
         widget=forms.TextInput(
              attrs={
                     'placeholder': 'Cash withdrawal international fee',
                     'class': 'form-control',
              }
         ),
         required=False,
    )

    balance_inquiry_fee = forms.CharField(
         label='Balance Inquiry Fee',
         widget=forms.TextInput(
              attrs={
                     'placeholder': 'Balance Inquiry Fee',
                     'class': 'form-control',
              }
         ),
         required=False,
    )

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super(CreateAtmForm, self).__init__(*args, **kwargs)
