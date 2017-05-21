# -*- coding: utf-8 -*-
"""
Context processors for base app
"""

from django.conf import settings
from django.contrib import messages

from base.api import api, APIError



def api_root(request):
    """Returns the configured API_ROOT"""
    return {'API_ROOT': settings.OAUTH_API + settings.OAUTH_API_BASE_PATH}



def api_username(request):
    """Returns the API username of the logged-in user"""
    username = 'not authenticated'
    if request.user.is_authenticated:
        try:
            data = api.get(request, '/users/current')
            username = data['username']
        except APIError as err:
            messages.error(request, err)
    return {'API_USERNAME': username}
