# -*- coding: utf-8 -*-
"""
Helpers to reuse common API calls
"""

from django.contrib import messages

from .api import api, APIError


def get_bank_id_choices(request):
    """Gets a list of bank ids and short_names as used by form choices"""
    choices = [('', 'Choose ...')]
    try:
        result = api.get(request, '/banks')
        for bank in result['banks']:
            choices.append((bank['id'], bank['short_name']))
    except APIError as err:
        messages.error(request, err)
    return choices


def get_user_id_choices(request):
    """Gets a list of user ids and usernames as used by form choices"""
    choices = [('', 'Choose ...')]
    try:
        result = api.get(request, '/users')
        for user in result['users']:
            choices.append((user['user_id'], user['username']))
    except APIError as err:
        messages.error(request, err)
    return choices
