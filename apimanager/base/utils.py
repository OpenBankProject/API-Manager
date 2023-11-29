# -*- coding: utf-8 -*-
"""
Base utilities
"""
from django.contrib.humanize.templatetags.humanize import naturaltime
from datetime import datetime, timedelta
from apimanager.settings import API_DATE_FORMAT_WITH_MILLISECONDS, API_DATE_FORMAT_WITH_DAY, \
    API_DATE_FORMAT_WITH_DAY_DATE_TIME
from base import context_processors
from django.contrib import messages
import functools
from obp.api import APIError, LOGGER
from django.http import JsonResponse
import traceback

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


def error_once_only(request, err):
    """
    Just add the error once
    :param request:
    :param err:
    :return:
    """
    LOGGER.exception('error_once_only - Error Message: {}'.format(err))
    storage = messages.get_messages(request)
    if str(err) not in [str(m.message) for m in storage]:
        messages.error(request, err)

def exception_handle(fn):
    @functools.wraps(fn)
    def wrapper(request, *args, **kwargs):
        try:
            result = fn(request, *args, **kwargs)
            if isinstance(result,dict) and 'code' in result and result['code'] >= 400:
                error_once_only(request, result['message'])
            else:
                msg = 'Submitted!'
                messages.success(request, msg)
        except APIError as err:
            error_once_only(request, APIError(Exception("OBP-API server is not running or do not response properly. "
                                                        "Please check OBP-API server.   Details: " + str(err))))
        except Exception as err:
            error_once_only(request, "Unknown Error. Details: " + str(err))
        return JsonResponse({'state': True})
    return wrapper

def convert_form_date_to_obpapi_datetime_format(form_to_date_string):
    """
       convert the String 2020-10-22 to 2020-10-22T00:00:00.000000Z
    """
    return datetime.strptime(form_to_date_string, API_DATE_FORMAT_WITH_DAY_DATE_TIME).strftime(API_DATE_FORMAT_WITH_MILLISECONDS)

def return_to_days_ago(date, days):
    """
       eg:
        date 2020-10-22T00:00:00.000000Z
        days =1
        return 2020-10-21T00:00:00.000000Z
    """
    return (datetime.strptime(date, API_DATE_FORMAT_WITH_MILLISECONDS) - timedelta(days)).strftime(API_DATE_FORMAT_WITH_MILLISECONDS)