"""
Forms of ATMs app
"""

from django import forms
from django.utils.translation import ugettext_lazy as _

import random


class CreateProductForm(forms.Form):

    parent_product_code = forms.CharField(
        label=_('Parent Product Code'),
        widget=forms.TextInput(
            attrs={
                'placeholder': 'parent_product_code-{}'.format(random.randint(1,1000)),
                'class': 'form-control',
            }
        ),
        initial='parent_product_code-{}'.format(random.randint(1,1000)),
    )

    name = forms.CharField(
        label=_('Account Name'),
        widget=forms.TextInput(
            attrs={
                'placeholder': _('The name of the Account'),
                'class': 'form-control',
            }
        ),
        required=True
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

    more_info_url= forms.CharField(
         label=_('More information URL'),
         widget=forms.TextInput(
             attrs={
                 'placeholder': _('www.example.com/abc'),
                 'class': 'form-control',
             }
         ),
         required=False,
    )
    terms_and_conditions_url = forms.CharField(
         label=_('Terms and Conditions'),
         widget=forms.TextInput(
              attrs={
                     'placeholder': _('www.example.com/xyz'),
                     'class': 'form-control',
              }
         ),
         required=False,
    )
    description = forms.CharField(
        label=_('Description'),
        widget=forms.TextInput(
           attrs={
                  'placeholder': _(''),
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
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super(CreateProductForm, self).__init__(*args, **kwargs)
