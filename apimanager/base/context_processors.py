# -*- coding: utf-8 -*-

from django.conf import settings

from base.utils import api_get


def api_root(request):
    return {'API_ROOT': settings.OAUTH_API + settings.OAUTH_API_BASE_PATH}

def api_username(request):
    if request.user.is_authenticated:
        data = api_get(request, '/users/current')
        api_username = data['username']
    else:
        api_username = 'not authenticated'
    return {'API_USERNAME': api_username}
