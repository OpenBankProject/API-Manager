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

    # This method will call '/my/logins/direct' endpoint and get the directLogin token back, store it to self.token filed.
    # the requestheaders are from the home.html form. eg:
    # username="susan.uk.29@example.com",password="2b78e8", consumer_key="my5qhma1cfig5wstj5poa355onjchk0enkf3boq4"
    def prepare_direct_login_token(self, requestheaders):
        """
        Logs into the API and returns the token

        data is a dict which contains keys username, password and consumer_key
        """
        url = settings.API_HOST + settings.DIRECTLOGIN_PATH
        authorization = 'DirectLogin username="{}",password="{}",consumer_key="{}"'.format(  # noqa
            requestheaders['username'],
            requestheaders['password'],
            requestheaders['consumer_key'])
        headers = {'Authorization': authorization}

        try:
            # 'http://127.0.0.1:8080/my/logins/direct'
            # Headers:{'Authorization': 'DirectLogin username="susan.uk.29@example.com",password="2b78e8",
            # consumer_key="my5qhma1cfig5wstj5poa355onjchk0enkf3boq4"'}
            # This will get the directLogin Token back.
            response = requests.post(url, headers=headers)
        except requests.exceptions.ConnectionError as err:
            raise AuthenticatorError(Exception("OBP-API server is not running or do not response properly. "
                                               "Please check OBP-API server.    "
                                               "Details: "+str(err)))
        except BaseException as err:
            raise AuthenticatorError(Exception("Unknown Error. Details:"+ str(err)))

        # This is the direct-Login Token:
        # <class 'dict'>: {'token': 'eyJhbGciOiJIUzI1NiJ9.eyIiOiIifQ.HURJVvyGgcPcjvrfRCSbRyk1_ssjlAUk8fP0leKx8kw'}
        result = response.json()
        if response.status_code != 201:
            raise AuthenticatorError(result['message'])
        else:
            self.token = result['token']

    def get_session(self):
        """Returns a session object to make authenticated requests"""
        headers = {'Authorization': 'DirectLogin token={}'.format(self.token)}
        session = requests.Session()
        session.headers.update(headers)
        return session
