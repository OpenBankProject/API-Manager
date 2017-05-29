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
