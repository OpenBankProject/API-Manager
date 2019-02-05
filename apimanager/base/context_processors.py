# -*- coding: utf-8 -*-
"""
Context processors for base app
"""

from django.conf import settings
from django.contrib import messages

from obp.api import API, APIError


def api_root(request):
    """Returns the configured API_ROOT"""
    return {'API_ROOT': settings.API_ROOT}


def api_username(request):
    """Returns the API username of the logged-in user"""
    username = 'not authenticated'
    if request.user.is_authenticated:
        try:
            api = API(request.session.get('obp'))
            data = api.get('/users/current')
            username = data['username']
        except APIError as err:
            messages.error(request, err)
        except Exception as err:
            messages.error(request, err)
    return {'API_USERNAME': username}


def api_user_id(request):
    """Returns the API user id of the logged-in user"""
    user_id = 'not authenticated'
    if request.user.is_authenticated:
        try:
            api = API(request.session.get('obp'))
            data = api.get('/users/current')
            user_id = data['user_id']
        except APIError as err:
            messages.error(request, err)
        except Exception as err:
            messages.error(request, err)
    return {'API_USER_ID': user_id}


def api_tester_url(request):
    """Returns the URL to the API Tester for the API instance"""
    url = getattr(settings, 'API_TESTER_URL', None)
    return {'API_TESTER_URL': url}
