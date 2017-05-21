# -*- coding: utf-8 -*-
"""
Module to handle the OBP API

It instantiates a convenience api object for imports, e.g.:
from base.api import api
"""

from datetime import datetime
import logging
import time

from requests.exceptions import ConnectionError
from requests_oauthlib import OAuth1Session

from django.conf import settings
from django.contrib.auth import logout



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

    def get(self, request, urlpath=''):
        """Gets data from the API"""
        return self.call(request, 'GET', urlpath)


    def delete(self, request, urlpath):
        """Deletes data from the API"""
        return self.call(request, 'DELETE', urlpath)


    def post(self, request, urlpath, payload):
        """Posts data to the API"""
        return self.call(request, 'POST', urlpath, payload)


    def put(self, request, urlpath, payload):
        """Puts data onto the API"""
        return self.call(request, 'PUT', urlpath, payload)


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


    def handle_response_error(self, request, prefix, error):
        if 'Invalid or expired access token' in error:
            logout(request)
        msg = '{} {}'.format(prefix, error)
        raise APIError(msg)


    def handle_response(self, request, response):
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
                self.handle_response_error(request, prefix, data['error'])
            return data


    def call(self, request, method='GET', urlpath='', payload=None):
        """Workhorse which actually calls the API"""
        url = settings.OAUTH_API + settings.OAUTH_API_BASE_PATH + urlpath
        log(logging.INFO, '{} {}'.format(method, url))
        if not hasattr(request, 'api'):
            request.api = OAuth1Session(
                settings.OAUTH_CONSUMER_KEY,
                client_secret=settings.OAUTH_CONSUMER_SECRET,
                resource_owner_key=request.session['oauth_token'],
                resource_owner_secret=request.session['oauth_secret']
            )
        time_start = time.time()
        try:
            if payload:
                response = request.api.request(method, url, json=payload)
            else:
                response = request.api.request(method, url)
        except ConnectionError as err:
            raise APIError(err)
        time_end = time.time()
        elapsed = int((time_end - time_start) * 1000)
        log(logging.INFO, 'Took {} ms'.format(elapsed))
        return self.handle_response(request, response)
api = API()
