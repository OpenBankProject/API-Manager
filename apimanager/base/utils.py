# -*- coding: utf-8 -*-

from datetime import datetime
import logging
import time
from requests_oauthlib import OAuth1Session

from django.conf import settings
from django.contrib.humanize.templatetags.humanize import naturaltime


DATE_FORMAT = '%d/%b/%Y %H:%M:%S'
LOGGER = logging.getLogger(__name__)


def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, datetime):
        serial = naturaltime(obj)
        return serial
    raise TypeError('Type not serializable')



def api_log(level, message):
    now = datetime.now().strftime(DATE_FORMAT)
    msg = '[{}] API: {}'.format(now, message)
    LOGGER.log(level, msg)


def api_get(request, urlpath=''):
    return api_call(request, 'GET', urlpath)


def api_post(request, urlpath, payload):
    return api_call(request, 'POST', urlpath, payload)


def api_put(request, urlpath, payload):
    return api_call(request, 'PUT', urlpath, payload)


def api_call(request, method='GET', urlpath='', payload=None):
    url = settings.OAUTH_API + settings.OAUTH_API_BASE_PATH + urlpath
    api_log(logging.INFO, '{} {}'.format(method, url))
    if not hasattr(request, 'api'):
        request.api = OAuth1Session(
            settings.OAUTH_CLIENT_KEY,
            client_secret=settings.OAUTH_CLIENT_SECRET,
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
    api_log(logging.INFO, 'Took {} ms'.format(elapsed))
    if response.status_code in [404, 500]:
        msg = 'Ran into a {}: {}'.format(response.status_code, response.text)
        api_log(logging.ERROR, msg)
        data = response.text
    else:
        data = response.json()
    return data
