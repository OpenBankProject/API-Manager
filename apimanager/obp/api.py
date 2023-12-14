# -*- coding: utf-8 -*-
"""
Module to handle the OBP API

It instantiates a convenience api object for imports, e.g.:
from obp.api import api
"""

from datetime import datetime
import importlib
import logging
import time

import requests
from requests.exceptions import ConnectionError

from django.conf import settings
from django.utils.translation import ugettext_lazy as _

DATE_FORMAT = '%d/%b/%Y %H:%M:%S'
LOGGER = logging.getLogger(__name__)


def log(level, message):
    """Logs a given message on a given level to log facility"""
    now = datetime.now().strftime(DATE_FORMAT)
    msg = '[{}] API: {}'.format(now, message)
    LOGGER.log(level, msg)


class APIError(Exception):
    """Exception class for API errors"""
    pass


class API(object):
    """Implements an interface to the OBP API"""
    session = None
    swagger = None

    def __init__(self, session_data=None):
        if session_data:
            self.start_session(session_data)
        self.session_data = session_data

    def call(self, method='GET', url='', payload=None, version=settings.API_VERSION['v500']):
        """Workhorse which actually calls the API"""
        log(logging.INFO, '{} {}'.format(method, url))
        if payload:
            log(logging.INFO, 'Payload: {}'.format(payload))
        # use `requests` if no session has been started
        session = self.session or requests
        time_start = time.time()
        try:
            if payload:
                response = session.request(method, url, json=payload, verify=settings.VERIFY)
            else:
                response = session.request(method, url, json={}, verify=settings.VERIFY)
        except ConnectionError as err:
            raise APIError(err)
        time_end = time.time()
        elapsed = int((time_end - time_start) * 1000)
        log(logging.INFO, 'Took {} ms'.format(elapsed))
        response.execution_time = elapsed
        return response

    def get(self, urlpath='', version=settings.API_VERSION['v500']):
        """
        Gets data from the API

        Convenience call which uses API_VERSION from settings
        """
        url = version + urlpath
        response = self.handle_response(self.call('GET', url))
        if response is not None and 'code' in response:
            raise APIError(response['message'])
        else:
            return response

    def delete(self, urlpath, version=settings.API_VERSION['v500']):
        """
        Deletes data from the API

        Convenience call which uses API_VERSION from settings
        """
        url = version + urlpath
        response = self.call('DELETE', url)
        return self.handle_response(response)

    def post(self, urlpath, payload, version=settings.API_VERSION['v500']):
        """
        Posts data to given urlpath with given payload

        Convenience call which uses API_VERSION from settings
        """
        url = version + urlpath
        response = self.call('POST', url, payload)
        return self.handle_response(response)

    def put(self, urlpath, payload, version=settings.API_VERSION['v500']):
        """
        Puts data on given urlpath with given payload

        Convenience call which uses API_VERSION from settings
        """
        url = version + urlpath
        response = self.call('PUT', url, payload)
        return self.handle_response(response)

    def handle_response_error(self, prefix, error):
        if 'Invalid or expired access token' in error:
            raise APIError(error)
        msg = '{} {}'.format(prefix, error)
        raise APIError(msg)

    def handle_response(self, response):
        """Handles the response, e.g. errors or conversion to JSON"""
        prefix = 'APIError'
        if response.status_code in [204]:
            return response.text
        else:
            data = response.json()
            if isinstance(data,dict) and 'error' in data:
                self.handle_response_error(prefix, data['error'])
        return data

    def start_session(self, session_data):
        """
        Starts a session with given session_data:
        - Authenticator class name (e.g. obp.oauth.OAuthAuthenticator)
        - Token data
        for subsequent requests to the API
        """
        if 'authenticator' in session_data and\
                'authenticator_kwargs' in session_data:
            mod_name, cls_name = session_data['authenticator'].rsplit('.', 1)
            log(logging.INFO, 'Authenticator {}'.format(cls_name))
            cls = getattr(importlib.import_module(mod_name), cls_name)
            authenticator = cls(**session_data['authenticator_kwargs'])
            self.session = authenticator.get_session()
            return self.session
        else:
            return None

    """ def get_swagger(self):
        Gets the swagger definition from the API
        # Poor man's caching ...
        if not self.session_data.get('swagger'):
            # API throws 500 if authenticated via GatewayLogin ...
            # response = self.call('GET', settings.API_URL_SWAGGER)
            response = requests.get(settings.API_URL_SWAGGER)
            swagger = self.handle_response(response)
            self.session_data['swagger'] = swagger
        return self.session_data.get('swagger') """

    def get_bank_id_choices(self):
        """Gets a list of bank ids and bank ids as used by form choices"""
        choices = [('', _('Choose ...'))]
        result = self.get('/banks')
        for bank in sorted(result['banks'], key=lambda d: d['id']) :
            choices.append((bank['id'], bank['id']))
        return choices

    def get_api_version_choices(self):
        """Gets a list of APIs Version and APIs Version as used by form choices"""
        choices = [('', _('Choose ...'))]
        result = self.get('/api/versions')
        for version in sorted(result['scanned_api_versions'], key=lambda d: d['API_VERSION']) :
            choices.append((version['API_VERSION'], version['API_VERSION']))
        return choices

    def get_user_id_choices(self):
        """Gets a list of user ids and usernames as used by form choices"""
        choices = [('', _('Choose ...'))]
        result = self.get('/users')
        for user in result['users']:
            choices.append((user['user_id'], user['username']))
        return choices