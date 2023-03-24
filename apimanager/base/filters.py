# -*- coding: utf-8 -*-
"""
Base filters
"""

from datetime import datetime, timedelta

from django.conf import settings


class BaseFilter(object):
    """Base for custom filter classes"""
    filter_type = None

    def __init__(self, context, request_get):
        self.context = context
        self.request_get = request_get

    def _apply(self, data, filter_value):
        """
        Actual application of filter
        Needs to be implemented by child class!
        """
        raise AttributeError('Not implemented yet!')

    def apply(self, data):
        """
        Apply filter to given data
        Also setup of context variables for templates
        """
        filter_all = 'active_{}_all'.format(self.filter_type)
        self.context[filter_all] = True
        filter_active_value = 'active_{}'.format(self.filter_type)
        self.context[filter_active_value] = 'All'

        if self.filter_type not in self.request_get:
            return data

        filter_value = self.request_get[self.filter_type]
        if not filter_value or filter_value == 'All':
            return data

        self.context[filter_all] = False
        self.context[filter_active_value] = filter_value
        filter_active = 'active_{}_{}'.format(self.filter_type, filter_value)
        self.context[filter_active] = True
        return self._apply(data, filter_value)


class FilterTime(BaseFilter):
    """Filter items by datetime"""
    filter_type = 'time'

    def __init__(self, context, request_get, time_fieldname):
        super().__init__(context, request_get)
        self.time_fieldname = time_fieldname

    def _apply(self, data, filter_value):
        if filter_value == 'minute':
            delta = timedelta(minutes=1)
        elif filter_value == 'hour':
            delta = timedelta(hours=1)
        elif filter_value == 'day':
            delta = timedelta(days=1)
        elif filter_value == 'week':
            delta = timedelta(days=7)
        elif filter_value == 'month':
            delta = timedelta(days=30)
        elif filter_value == 'year':
            delta = timedelta(days=365)
        else:
            return data

        now = datetime.utcnow()
        filtered = []
        print("FILTERED")
        print(filtered)
        for item in data:
            item_date = datetime.strptime(
                item[self.time_fieldname], settings.API_DATE_FORMAT_WITH_MILLISECONDS)
            if now - item_date <= delta:
                filtered.append(item)
        return filtered
