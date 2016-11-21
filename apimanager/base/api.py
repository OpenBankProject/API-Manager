# -*- coding: utf-8 -*-

from datetime import datetime
import logging
import time
from requests_oauthlib import OAuth1Session

from django.conf import settings

DATE_FORMAT = '%d/%b/%Y %H:%M:%S'
LOGGER = logging.getLogger(__name__)


class API(object):

    def log(self, level, message):
        now = datetime.now().strftime(DATE_FORMAT)
        msg = '[{}] API: {}'.format(now, message)
        LOGGER.log(level, msg)


    def get(self, request, urlpath=''):
        return self.call(request, 'GET', urlpath)


    def delete(self, request, urlpath):
        return self.call(request, 'DELETE', urlpath)


    def post(self, request, urlpath, payload):
        return self.call(request, 'POST', urlpath, payload)


    def put(self, request, urlpath, payload):
        return self.call(request, 'PUT', urlpath, payload)


    def call(self, request, method='GET', urlpath='', payload=None):
        url = settings.OAUTH_API + settings.OAUTH_API_BASE_PATH + urlpath
        self.log(logging.INFO, '{} {}'.format(method, url))
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
        self.log(logging.INFO, 'Took {} ms'.format(elapsed))
        if response.status_code in [404, 500]:
            msg = 'Ran into a {}: {}'.format(response.status_code, response.text)
            self.log(logging.ERROR, msg)
            data = response.text
        elif response.status_code in [204]:
            data = response.text
        else:
            data = response.json()
        return data


api = API()
