# -*- coding: utf-8 -*-
"""
Context processors for base app
"""

from django.conf import settings
from django.contrib import messages

from obp.api import API, APIError



def api_root(request):
    """Returns the configured API_ROOT"""
    return {'API_ROOT': settings.API_HOST + settings.API_BASE_PATH}



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
    return {'API_USERNAME': username}
