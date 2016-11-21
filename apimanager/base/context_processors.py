# -*- coding: utf-8 -*-
"""
Context processors for base app
"""

from django.conf import settings

from base.api import api



def api_root(request):
    """Returns the configured API_ROOT"""
    return {'API_ROOT': settings.OAUTH_API + settings.OAUTH_API_BASE_PATH}



def api_username(request):
    """Returns the API username of the logged-in user"""
    if request.user.is_authenticated:
        data = api.get(request, '/users/current')
        username = data['username']
    else:
        username = 'not authenticated'
    return {'API_USERNAME': username}
