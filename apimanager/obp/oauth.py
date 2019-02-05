# -*- coding: utf-8 -*-
"""
OAuth authenticator for OBP app
"""

import logging

from django.conf import settings

from requests.exceptions import ConnectionError
from requests_oauthlib import OAuth1Session
from requests_oauthlib.oauth1_session import TokenRequestDenied

from .authenticator import Authenticator, AuthenticatorError


LOGGER = logging.getLogger(__name__)


class OAuthAuthenticator(Authenticator):
    """Implements an OAuth authenticator to the API"""

    token = None
    secret = None

    def __init__(self, token=None, secret=None):
        self.token = token
        self.secret = secret

    def get_authorization_url(self, callback_uri):
        session = OAuth1Session(
            settings.OAUTH_CONSUMER_KEY,
            client_secret=settings.OAUTH_CONSUMER_SECRET,
            callback_uri=callback_uri,
        )
        try:
            url = settings.API_HOST + settings.OAUTH_TOKEN_PATH
            response = session.fetch_request_token(url, verify=False)
        except (ValueError, TokenRequestDenied, ConnectionError) as err:
            raise AuthenticatorError(err)
        else:
            self.token = response.get('oauth_token')
            self.secret = response.get('oauth_token_secret')
        url = settings.API_HOST + settings.OAUTH_AUTHORIZATION_PATH
        authorization_url = session.authorization_url(url)
        LOGGER.log(logging.INFO, 'Initial token {}, secret {}'.format(
            self.token, self.secret))
        return authorization_url

    def set_access_token(self, authorization_url):
        session = OAuth1Session(
            settings.OAUTH_CONSUMER_KEY,
            settings.OAUTH_CONSUMER_SECRET,
            resource_owner_key=self.token,
            resource_owner_secret=self.secret,
        )
        session.parse_authorization_response(authorization_url)
        url = settings.API_HOST + settings.OAUTH_ACCESS_TOKEN_PATH
        try:
            response = session.fetch_access_token(url)
        except (TokenRequestDenied, ConnectionError) as err:
            raise AuthenticatorError(err)
        else:
            self.token = response.get('oauth_token')
            self.secret = response.get('oauth_token_secret')
        LOGGER.log(logging.INFO, 'Updated token {}, secret {}'.format(
            self.token, self.secret))

    def get_session(self):
        session = OAuth1Session(
            settings.OAUTH_CONSUMER_KEY,
            client_secret=settings.OAUTH_CONSUMER_SECRET,
            resource_owner_key=self.token,
            resource_owner_secret=self.secret,
        )
        return session
