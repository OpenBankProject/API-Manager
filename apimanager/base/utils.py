# -*- coding: utf-8 -*-
"""
Base utilities
"""

from datetime import datetime
from django.contrib.humanize.templatetags.humanize import naturaltime


def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, datetime):
        serial = naturaltime(obj)
        return serial
    raise TypeError('Type not serializable')
