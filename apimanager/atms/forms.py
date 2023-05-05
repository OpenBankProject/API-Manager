"""
Forms of ATMs app
"""

from django import forms
from django.utils.translation import ugettext_lazy as _

import random


class CreateAtmForm(forms.Form):

    ATTRIBUTE_TYPE = (
        ('', _('Any')),
        ('STRING', 'STRING'),
        ('INTEGER', 'INTEGER'),
        ('DOUBLE', 'DOUBLE'),
        ('DATE_WITH_DAY', 'DATE_WITH_DAY'),
    )

    atm_id = forms.CharField(
        label=_('ATM Id'),
        widget=forms.TextInput(
            attrs={
                'placeholder': 'atm-id-{}'.format(random.randint(1,1000)),
                'class': 'form-control',
            }
        ),
        initial='atm-id-{}'.format(random.randint(1,1000)),
    )

    bank_id = forms.ChoiceField(
        label=_('Bank Id'),
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
                'placeholder': _('The name of the ATM'),
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
                'placeholder': " ",
                'class': 'form-control',
            }
        ),
        required=False,
    )

    location_longitude = forms.FloatField(
        label=_('Longitude'),
        widget=forms.TextInput(
            attrs={
                'placeholder': " ",
                'class': 'form-control',
            }
        ),
        required=False,
    )

    meta_license_id = forms.CharField(
        label=_('Meta License Id'),
        widget=forms.TextInput(
            attrs={
                'placeholder': 'PDDL',
                'class': 'form-control',
            }
        ),
        required=False,
    )

    meta_license_name = forms.CharField(
        label=_('Meta License Name'),
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Open Data Commons Public Domain Dedication and License',
                'class': 'form-control',
            }
        ),
        required=False,
    )

    lobby = forms.CharField(
        label=_('Opening Hours'),
        widget=forms.Textarea(
            attrs={
                'placeholder': 'None',
                'class': 'form-control',
            }
        ),
        required=False,
    )
    monday = forms.CharField(
           label=_('Monday'),
           widget=forms.TextInput(
               attrs={
                   'placeholder': 'None',
                   'class': 'form-control',
               }
           ),
           required=False,
       )
    tuesday = forms.CharField(
           label=_('Tuesday'),
           widget=forms.TextInput(
               attrs={
                   'placeholder': 'None',
                   'class': 'form-control',
               }
           ),
           required=False,
       )
    wednesday = forms.CharField(
           label=_('Wednesday'),
           widget=forms.TextInput(
               attrs={
                   'placeholder': 'None',
                   'class': 'form-control',
               }
           ),
           required=False,
       )
    thursday = forms.CharField(
           label=_('Thursday'),
           widget=forms.TextInput(
               attrs={
                   'placeholder': 'None',
                   'class': 'form-control',
               }
           ),
           required=False,
       )
    friday = forms.CharField(
           label=_('Friday'),
           widget=forms.TextInput(
               attrs={
                   'placeholder': 'None',
                   'class': 'form-control',
               }
           ),
           required=False,
       )
    saturday = forms.CharField(
           label=_('Saturday'),
           widget=forms.TextInput(
               attrs={
                   'placeholder': 'None',
                   'class': 'form-control',
               }
           ),
           required=False,
       )
    sunday = forms.CharField(
           label=_('Sunday'),
           widget=forms.TextInput(
               attrs={
                   'placeholder': 'None',
                   'class': 'form-control',
               }
           ),
           required=False,
       )
    is_accessible = forms.ChoiceField(
            label=_('Is Accessible'),
            widget=forms.Select(
                attrs={
                    'class': 'form-control',
                }
            ),
            required=False,
        )
    located_at = forms.CharField(
        label=_('ATM Location'),
        widget=forms.TextInput(
            attrs={
                'placeholder': 'OBP',
                'class': 'form-control',
            }
        ),
        required=False,
    )
    more_info = forms.CharField(
            label=_('More Information'),
            widget=forms.TextInput(
                attrs={
                    'placeholder': _('short walk to the lake from here'),
                    'class': 'form-control',
                }
            ),
            required=False,
       )
    has_deposit_capability = forms.ChoiceField(
             label=_('Deposit Capabilities'),
             widget=forms.Select(
                  attrs={
                         'class': 'form-control',
                  }
             ),
             required=False,
        )
    supported_languages = forms.CharField(
            label=_('Supported Languages'),
            widget=forms.TextInput(
               attrs={
                      'class': 'form-control',
               }
            ),
            required=False,
        )
    services = forms.CharField(
            label=_('Services'),
            widget=forms.TextInput(
                attrs={
                    'placeholder': _('Services'),
                    'class': 'form-control',
                }
            ),
            required=False,
        )
    accessibility_features = forms.CharField(
        label=_('Accessible Features'),
        widget=forms.TextInput(
            attrs={
                'placeholder': _('wheelchair, atm usuable by the visually impaired'),
                'class': 'form-control',
            }
        ),
        required=False,
    )
    supported_currencies = forms.CharField( # not be a dropdown
        label=_('Supported Currencies'),
        widget=forms.TextInput(
            attrs={
                'placeholder': _('Currency'),
                'class': 'form-control',
            }
        ),
        required=False,
    )
    notes = forms.CharField(
        label=_('Notes'),
        widget=forms.TextInput(
            attrs={
               'placeholder': _('Notes'),
               'class': 'form-control',
            }
        ),
        required=False,
    )
    type_attribute = forms.ChoiceField(
        label=_('Type'),
        choices=ATTRIBUTE_TYPE,
        widget=forms.Select(
            attrs={
               'class': 'form-control bank_attribute_type',
            }
        ),
        required=False,
    )

    location_categories = forms.CharField(
        label=_('Location Category'),
        widget=forms.TextInput(
           attrs={
              'placeholder': _('Location Category'),
              'class': 'form-control',
           }
        ),
        required=False,
    )
    minimum_withdrawal = forms.CharField(
        label=_('Minimum Withdrawal'),
        widget=forms.TextInput(
            attrs={
                'placeholder': '5',
                 'class': 'form-control',
            }
        ),
        required=False,
    )
    branch_identification = forms.CharField(
            label=_('Branch Identification'),
            widget=forms.TextInput(
                attrs={
                    'placeholder': _('Enter your Branch Identification'),
                    'class': 'form-control',
                }
            ),
            required=False,
        )
    site_identification = forms.CharField(
            label=_('Site Identification'),
            widget=forms.TextInput(
                attrs={
                   'placeholder': _('Enter your Site Identification'),
                   'class': 'form-control',
                }
            ),
            required=False,
        )
    site_name = forms.CharField(
        label=_('Site Name'),
        widget=forms.TextInput(
            attrs={
               'placeholder': _('Enter your Site Name '),
               'class': 'form-control',
            }
        ),
        required=False,
    )
    cash_withdrawal_national_fee = forms.CharField(
         label=_('Cash Withdrawal National Fee'),
         widget=forms.TextInput(
              attrs={
                     'placeholder': _('Cash withdrawal national fee'),
                     'class': 'form-control',
              }
         ),
         required=False,
    )
    cash_withdrawal_international_fee = forms.CharField(
         label=_('Cash Withdrawal International Fee'),
         widget=forms.TextInput(
              attrs={
                     'placeholder': _('Cash withdrawal international fee'),
                     'class': 'form-control',
              }
         ),
         required=False,
    )
    balance_inquiry_fee = forms.CharField(
         label=_('Balance Inquiry Fee'),
         widget=forms.TextInput(
              attrs={
                     'placeholder': _('Balance Inquiry Fee'),
                     'class': 'form-control',
              }
         ),
         required=False,
    )

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super(CreateAtmForm, self).__init__(*args, **kwargs)
