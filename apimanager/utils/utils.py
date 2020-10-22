# -*- coding: utf-8 -*-
"""
Base utilities
"""

from datetime import datetime
from django.contrib.humanize.templatetags.humanize import naturaltime
from base import context_processors


def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, datetime):
        serial = naturaltime(obj)
        return serial
    raise TypeError('Type not serializable')

def get_cache_key_for_current_call(request, urlpath):
    """we will generate the cache key by login username+urlpath
       url path may contain lots of special characters, here we use the hash method first.
    """
    return context_processors.api_username(request).get('API_USERNAME') + str(hash(urlpath)) 