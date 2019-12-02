from django.contrib import messages
import functools
from obp.api import API, APIError
from django.http import JsonResponse
import traceback

def error_once_only(request, err):
    """
    Just add the error once
    :param request:
    :param err:
    :return:
    """
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
                msg = 'Submit successfully!'
                messages.success(request, msg)
        except APIError as err:
            error_once_only(request, APIError(Exception("OBP-API server is not running or do not response properly. "
                                                        "Please check OBP-API server.   Details: " + str(err))))
        except Exception as err:
            error_once_only(request, "Unknown Error. Details: " + str(err))
        return JsonResponse({'state': True})
    return wrapper