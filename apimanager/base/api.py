# -*- coding: utf-8 -*-
"""
Module to handle the OBP API

It instantiates a convenience api object for imports, e.g.:
from base.api import api
"""

from datetime import datetime
import logging
import time
from requests_oauthlib import OAuth1Session

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


    def handle_response(self, response):
        """Handles the response, e.g. errors or conversion to JSON"""
        prefix = 'APIError'
        if response.status_code in [404, 500]:
            msg = '{} {}: {}'.format(
                prefix, response.status_code, response.text)
            log(logging.ERROR, msg)
            raise APIError(msg)
        elif response.status_code in [204]:
            return response.text
        else:
            data = response.json()
            if 'error' in data:
                msg = '{} {}'.format(prefix, data['error'])
                raise APIError(msg)
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
        if payload:
            response = request.api.request(method, url, json=payload)
        else:
            response = request.api.request(method, url)
        time_end = time.time()
        elapsed = int((time_end - time_start) * 1000)
        log(logging.INFO, 'Took {} ms'.format(elapsed))
        return self.handle_response(response)
api = API()
