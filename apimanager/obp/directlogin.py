# -*- coding: utf-8 -*-
"""
DirectLogin authenticator for OBP app
"""


import requests

from django.conf import settings

from .authenticator import Authenticator, AuthenticatorError


class DirectLoginAuthenticator(Authenticator):
    """Implements a DirectLogin authenticator to the API"""

    token = None

    def __init__(self, token=None):
        self.token = token

    def login_to_api(self, data):
        """
        Logs into the API and returns the token

        data is a dict which contains keys username, password and consumer_key
        """
        url = settings.API_HOST + settings.DIRECTLOGIN_PATH
        authorization = 'DirectLogin username="{}",password="{}",consumer_key="{}"'.format(  # noqa
            data['username'],
            data['password'],
            data['consumer_key'])
        headers = {'Authorization': authorization}

        try:
            response = requests.post(url, headers=headers)
        except requests.exceptions.ConnectionError as err:
            raise AuthenticatorError(err)

        result = response.json()
        if response.status_code != 201:
            raise AuthenticatorError(result['error'])
        else:
            self.token = result['token']

    def get_session(self):
        """Returns a session object to make authenticated requests"""
        headers = {'Authorization': 'DirectLogin token={}'.format(self.token)}
        session = requests.Session()
        session.headers.update(headers)
        return session
