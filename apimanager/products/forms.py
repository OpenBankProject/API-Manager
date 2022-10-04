"""
Forms of branches app
"""

from django import forms
from django.utils.translation import ugettext_lazy as _
import random


class CreateProductForm(forms.Form):

    product_code = forms.CharField(
        label=_('Product Code'),
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Product-Code-{}'.format(random.randint(1,1000)),
                'class': 'form-control',
            }
        ),
        initial='Product-Code-{}'.format(random.randint(1,1000)),
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

    parent_product_code = forms.CharField(
        label=_('parent_product_code'),
        widget=forms.TextInput(
            attrs={
                'placeholder': _('parent_product_code'),
                'class': 'form-control',
            }
        ),
        required=False
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
    more_info_url = forms.CharField(
        label=_('more_info_url'),
        widget=forms.TextInput(
            attrs={
                'placeholder': _('The name of the branch'),
                'class': 'form-control',
            }
        ),
        required=False
    )
    terms_and_conditions_url = forms.CharField(
        label=_('terms_and_conditions_url'),
        widget=forms.TextInput(
            attrs={
                'placeholder': _('terms_and_conditions_url'),
                'class': 'form-control',
            }
        ),
        required=False
    )
    description = forms.CharField(
        label=_('description'),
        widget=forms.TextInput(
            attrs={
                'placeholder': _('description'),
                'class': 'form-control',
            }
        ),
        required=False
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

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super(CreateProductForm, self).__init__(*args, **kwargs)
