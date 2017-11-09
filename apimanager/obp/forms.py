# -*- coding: utf-8 -*-
"""
Forms for OBP app
"""

from django import forms

from .authenticator import AuthenticatorError
from .directlogin import DirectLoginAuthenticator
from .gatewaylogin import GatewayLoginAuthenticator


class DirectLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control'}))
    consumer_key = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control'}))

    def clean(self):
        """
        Stores an authenticator in cleaned_data after successful login to API
        """
        cleaned_data = super(DirectLoginForm, self).clean()
        authenticator = DirectLoginAuthenticator()
        try:
            authenticator.login_to_api(cleaned_data)
            cleaned_data['authenticator'] = authenticator
        except AuthenticatorError as err:
            raise forms.ValidationError(err)
        return cleaned_data


class GatewayLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    secret = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control'}))

    def clean(self):
        """
        Stores an authenticator in cleaned_data after successful login to API
        """
        cleaned_data = super(GatewayLoginForm, self).clean()
        authenticator = GatewayLoginAuthenticator()
        try:
            authenticator.login_to_api(cleaned_data)
            cleaned_data['authenticator'] = authenticator
        except AuthenticatorError as err:
            raise forms.ValidationError(err)
        return cleaned_data
