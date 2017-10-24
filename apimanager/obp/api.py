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
        self.set_base_path()
        if session_data:
            self.start_session(session_data)
        self.session_data = session_data

    def set_base_path(self, base_path=None):
        """Sets the basepath for API calls"""
        if base_path:
            self.base_path = settings.API_HOST + base_path
        else:
            self.base_path = settings.API_HOST + settings.API_BASE_PATH

    def call(self, method='GET', urlpath='', payload=None):
        """Workhorse which actually calls the API"""
        url = self.base_path + urlpath
        log(logging.INFO, '{} {}'.format(method, url))
        if payload:
            log(logging.INFO, 'Payload: {}'.format(payload))
        # use `requests` if no session has been started
        session = self.session or requests
        time_start = time.time()
        try:
            if payload:
                response = session.request(method, url, json=payload)
            else:
                response = session.request(method, url)
        except ConnectionError as err:
            raise APIError(err)
        time_end = time.time()
        elapsed = int((time_end - time_start) * 1000)
        log(logging.INFO, 'Took {} ms'.format(elapsed))
        response.execution_time = elapsed
        return response

    def get(self, urlpath=''):
        """Gets data from the API"""
        response = self.call('GET', urlpath)
        return self.handle_response(response)

    def delete(self, urlpath):
        """Deletes data from the API"""
        response = self.call('DELETE', urlpath)
        return self.handle_response(response)

    def post(self, urlpath, payload):
        """Posts data to the API"""
        response = self.call('POST', urlpath, payload)
        return self.handle_response(response)

    def put(self, urlpath, payload):
        """Puts data onto the API"""
        response = self.call('PUT', urlpath, payload)
        return self.handle_response(response)

    def handle_response_404(self, response, prefix):
        # Stripping HTML body ...
        if response.text.find('body'):
            msg = response.text.split('<body>')[1].split('</body>')[0]
        msg = '{} {}: {}'.format(
            prefix, response.status_code, msg)
        log(logging.ERROR, msg)
        raise APIError(msg)

    def handle_response_500(self, response, prefix):
        msg = '{} {}: {}'.format(
            prefix, response.status_code, response.text)
        log(logging.ERROR, msg)
        raise APIError(msg)

    def handle_response_error(self, prefix, error):
        if 'Invalid or expired access token' in error:
            raise APIError(error)
        msg = '{} {}'.format(prefix, error)
        raise APIError(msg)

    def handle_response(self, response):
        """Handles the response, e.g. errors or conversion to JSON"""
        prefix = 'APIError'
        if response.status_code == 404:
            self.handle_response_404(response, prefix)
        elif response.status_code == 500:
            self.handle_response_500(response, prefix)
        elif response.status_code in [204]:
            return response.text
        else:
            data = response.json()
            if 'error' in data:
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

    def get_swagger(self):
        """Gets the swagger definition from the API"""
        if not self.session_data.get('swagger'):
            self.set_base_path(settings.API_SWAGGER_BASE_PATH)
            urlpath = '/resource-docs/v3.0.0/swagger'
            response = self.get(urlpath)
            # Set base path back
            self.set_base_path()
            self.session_data['swagger'] = response
        return self.session_data.get('swagger')

    def get_bank_id_choices(self):
        """Gets a list of bank ids and bank ids as used by form choices"""
        choices = [('', 'Choose ...')]
        result = self.get('/banks')
        for bank in result['banks']:
            choices.append((bank['id'], bank['id']))
        return choices

    def get_user_id_choices(self):
        """Gets a list of user ids and usernames as used by form choices"""
        choices = [('', 'Choose ...')]
        result = self.get('/users')
        for user in result['users']:
            choices.append((user['user_id'], user['username']))
        return choices
