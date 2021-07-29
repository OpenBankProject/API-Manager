# -*- coding: utf-8 -*-
"""
Context processors for base app
"""

from django.conf import settings
from django.contrib import messages

from obp.api import API, APIError, LOGGER
from django.core.cache import cache


def api_root(request):
    """Returns the configured API_ROOT"""
    return {'API_ROOT': settings.API_ROOT}


def portal_page(request):
    """Returns the configured API_PORTAL"""
    if settings.API_PORTAL is None:
        return {'API_PORTAL': settings.API_HOST}
    else:
        return {'API_PORTAL': settings.API_PORTAL}


def logo_url(request):
    """Returns the configured LOGO_URL"""
    return {'logo_url': settings.LOGO_URL}


def api_username(request):
    """Returns the API username/email of the logged-in user"""
    nametodisplay = 'not authenticated'
    get_current_user_api_url = '/users/current'
    #Here we can not get the user from obp-api side, so we use the django auth user id here. 
    cache_key_django_user_id = request.session._session.get('_auth_user_id')
    cache_key = '{},{},{}'.format('api_username',get_current_user_api_url, cache_key_django_user_id)
    apicaches=None
    try:
        apicaches=cache.get(cache_key)
    except Exception as err:
        apicaches=None
    if not apicaches is None:
        return apicaches
    else:
        if request.user.is_authenticated:
            try:
                api = API(request.session.get('obp'))
                data = api.get(get_current_user_api_url)
                username = data['username']
                email = data['email']
                provider = data['provider']
                if "google" in provider:
                    nametodisplay = email
                elif "yahoo" in provider:
                    nametodisplay = email
                else:
                    nametodisplay = username
                apicaches=cache.set(cache_key, {'API_USERNAME': nametodisplay})
                LOGGER.warning('The cache is setting try to api_user_name:')
                LOGGER.warning('The cache is setting key is: {}'.format(cache_key))
            except APIError as err:
                messages.error(request, err)
            except Exception as err:
                messages.error(request, err)
        return {'API_USERNAME': nametodisplay}


def api_user_id(request):
    """Returns the API user id of the logged-in user"""
    user_id = 'not authenticated'
    get_current_user_api_url = '/users/current'
    #Here we can not get the user from obp-api side, so we use the django auth user id here. 
    cache_key_django_user_id = request.session._session.get('_auth_user_id')
    cache_key = '{},{},{}'.format('api_user_id',get_current_user_api_url, cache_key_django_user_id)
    apicaches=None
    try:
        apicaches=cache.get(cache_key)
    except Exception as err:
        apicaches=None
    if not apicaches is None:
        return apicaches
    else:
        if request.user.is_authenticated:
            try:
                api = API(request.session.get('obp'))
                data = api.get('/users/current')
                user_id = data['user_id']
                apicaches=cache.set(cache_key, {'API_USER_ID': user_id})
                LOGGER.warning('The cache is setting try to api_user_id:')
                LOGGER.warning('The cache is setting key is: {}'.format(cache_key))
            except APIError as err:
                messages.error(request, err)
            except Exception as err:
                messages.error(request, err)
        return {'API_USER_ID': user_id}


def api_tester_url(request):
    """Returns the URL to the API Tester for the API instance"""
    url = getattr(settings, 'API_TESTER_URL', None)
    return {'API_TESTER_URL': url}
