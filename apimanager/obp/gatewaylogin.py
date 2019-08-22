# -*- coding: utf-8 -*-
"""
GatewayLogin authenticator for OBP app
"""


import jwt
import requests

from django.conf import settings

from .authenticator import Authenticator, AuthenticatorError


class GatewayLoginAuthenticator(Authenticator):
    """Implements a GatewayLogin authenticator to the API"""

    token = None

    def __init__(self, token=None):
        self.token = token

    def create_jwt(self, data):
        """
        Creates a JWT used for future requests tothe API
        data is a dict which contains keys username, secret
        """
        message = {
            'login_user_name': data['username'],
            'time_stamp': 'unused',
            'app_id': '',  # Do not create new consumer
            'app_name': '',  # Do not create new consumer
            'temenos_id': '',  # Whatever that does
        }
        if settings.GATEWAYLOGIN_HAS_CBS:
            # Not sure if that is the right thing to do
            message['is_first'] = True
        else:
            # Fake when there is no core banking system
            message.update({
                'is_first': False,
                'cbs_token': 'dummy',
            })
        token = jwt.encode(message, data['secret'], 'HS256')
        self.token = token.decode('utf-8')
        return self.token

    def prepare_gateway_login_token(self, data):
        token = self.create_jwt(data)
        # Make a test call to see if the token works
        url = '{}{}'.format(settings.API_ROOT, '/users/current')
        api = self.get_session()
        try:
            response = api.get(url)
        except requests.exceptions.ConnectionError as err:
            raise AuthenticatorError(Exception("The OBP-API server is not running or does not respond properly."
                                               "Please check OBP-API server.    "
                                               "Details: " + str(err)))
        except BaseException as err:
            raise AuthenticatorError(Exception("Unknown Error. Details:" + str(err)))
        # this will show the obp errors
        if response.status_code != 200:
            raise AuthenticatorError(response.json()['message'])
        else:
            return token

    def get_session(self):
        """Returns a session object to make authenticated requests"""
        headers = {
            'Authorization': 'GatewayLogin token="{}"'.format(self.token),
        }
        session = requests.Session()
        session.headers.update(headers)
        return session
