# -*- coding: utf-8 -*-
"""
Views of metrics app
"""

import json
import hashlib
import operator
from datetime import datetime, timedelta
from enum import Enum

from django.conf import settings
from django.http import JsonResponse
from apimanager import local_settings
from apimanager.settings import API_HOST, EXCLUDE_APPS, EXCLUDE_FUNCTIONS, EXCLUDE_URL_PATTERN, API_EXPLORER_APP_NAME, API_DATE_FORMAT_WITH_MILLISECONDS, API_DATE_FORMAT_WITH_SECONDS , DEBUG
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from base.utils import error_once_only, get_cache_key_for_current_call, convert_form_date_to_obpapi_datetime_format, \
    return_to_days_ago
from obp.api import API, APIError, LOGGER
from .forms import APIMetricsForm, ConnectorMetricsForm, MonthlyMetricsSummaryForm, CustomSummaryForm
from pylab import *
from django.core.cache import cache
from base.views import get_consumers, get_api_versions
import traceback
try:
    # Python 2
    import cStringIO
except ImportError:
    # Python 3
    import io
import base64
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import statistics
import urllib.parse


CACHE_SETTING_URL_MSG = "The cache setting url is"
CACHE_SETTING_KEY_MSG = "The cache setting key is"

def get_random_color(to_hash):
    hashed = str(int(hashlib.md5(to_hash.encode('utf-8')).hexdigest(), 16))
    r = int(hashed[0:3]) % 255
    b = int(hashed[3:6]) % 255
    g = int(hashed[6:9]) % 255
    return 'rgba({}, {}, {}, 0.3)'.format(r, g, b)

def get_barchart_data(metrics, fieldname):
    """
    Gets bar chart data compatible with Chart.js from the field with given
    fieldname in given metrics
    """
    border_color = 'rgba(0, 0, 0, 1)'
    data = {
        'labels': [],
        'data': [],
        'backgroundColor': [],
        'borderColor': [],
    }
    items = {}
    for metric in metrics:
        if not metric[fieldname]:
            continue
        if metric[fieldname] in items:
            items[metric[fieldname]] += 1
        else:
            items[metric[fieldname]] = 1
    sorted_items = sorted(
            items.items(), key=operator.itemgetter(1), reverse=True)
    for item in sorted_items:
        data['labels'].append(item[0])
        data['data'].append(item[1])
        data['backgroundColor'].append(get_random_color(item[0]))
        data['borderColor'].append(border_color)
    return data


class SummaryType(Enum):
    YEARLY = 1
    QUARTERLY = 2
    MONTHLY = 3
    WEEKLY = 4
    DAILY = 5
    CUSTOM = 6

class MetricsView(LoginRequiredMixin, TemplateView):
    """View for metrics (sort of abstract base class)"""
    form_class = None
    template_name = None
    api_urlpath = None

    def get_form(self):
        """
        Get bound form either from request.GET or initials
        We need a bound form because we already send a request to the API
        without user intervention on initial request
        """
        if self.request.GET:
            data = self.request.GET
        else:
            fields = self.form_class.declared_fields
            data = {}
            for name, field in fields.items():
                if field.initial:
                    data[name] = field.initial
        form = self.form_class(data)
        return form

    def to_django(self, metrics):
        """
        Convert metrics data from API to format understood by Django
        - Make datetime out of string in field 'date'
        """
        for metric in metrics:
            metric['date'] = datetime.datetime.strptime(
                metric['date'], settings.API_DATE_FORMAT_WITH_SECONDS )
        return metrics

    def to_api(self, cleaned_data):
        """
        Convert form data from Django to format understood by API
        - API treats empty parameters as actual values, so we have to remove
        them
        - Need to convert datetimes into required format
        """
        params = []
        for name, value in cleaned_data.items():
            # Maybe we should define the API format as Django format to not
            # have to convert in places like this?
            if value.__class__.__name__ == 'datetime':
                value = value.strftime(settings.API_DATE_FORMAT_WITH_MILLISECONDS)
            if value:
                # API does not like quoted data
                params.append('{}={}'.format(name, value))
        params = '&'.join(params)
        return params

    def get_metrics(self, cleaned_data):
        """
        Gets the metrics from the API, using given cleaned form data.
        """
        metrics = []
        params = self.to_api(cleaned_data)
        urlpath = '{}?{}'.format(self.api_urlpath, params)
        api = API(self.request.session.get('obp'))
        try:
            metrics = api.get(urlpath, version=settings.API_VERSION["v510"])
            metrics = self.to_django(metrics['metrics'])
        except APIError as err:
            error_once_only(self.request, err)
        except KeyError as err:
            error_once_only(self.request, metrics['message'])
        except Exception as err:
            error_once_only(self.request, err)
        return metrics

    def get_context_data(self, **kwargs):
        context = super(MetricsView, self).get_context_data(**kwargs)
        metrics = []
        form = self.get_form()
        if form.is_valid():
            metrics = self.get_metrics(form.cleaned_data)
        context.update({
            'metrics': metrics,
            'form': form,
        })
        return context


class APIMetricsView(MetricsView):
    """View for API metrics"""
    form_class = APIMetricsForm
    template_name = 'metrics/api.html'
    api_urlpath = '/management/metrics'

    def dispatch(self, request, *args, **kwargs):
        self.api = API(request.session.get('obp'))
        return super(APIMetricsView, self).dispatch(request, *args, **kwargs)

    def get_form(self, *args, **kwargs):
        form = super(APIMetricsView, self).get_form(*args, **kwargs)
        # Cannot add api in constructor: super complains about unknown kwarg
        form.api = self.api
        fields = form.fields
        try:
            fields['consumer_id'].choices = self.api.get_consumer_id_choices()
            fields['implemented_in_version'].choices = self.api.get_api_version_choices()
        except APIError as err:
            messages.error(self.request, err)
        except Exception as err:
            messages.error(self.request, err)
        return form

    def get_context_data(self, **kwargs):
        context = super(APIMetricsView, self).get_context_data(**kwargs)
        context.update({
            'consumer_id': get_consumers(self.request),
            'API_VERSION': get_api_versions(self.request)
        })
        return context

def get_metric_last_endpoint(request):
    to_date = datetime.datetime.now().strftime(settings.API_DATE_FORMAT_WITH_MILLISECONDS)
    urlpath = "/management/metrics?limit=1&to_date="+to_date
    api = API(request.session.get('obp'))
    last_endpoint_metric={}
    try:
        metric = api.get(urlpath)['metrics'][0]
        last_endpoint_metric={
            'implemented_by_partial_function':metric['implemented_by_partial_function'],
            'duration': metric['duration'], 
            'date': metric['date'], 
            'verb': metric['verb'],
            'url': metric['url']
        }
    except Exception as err:
        LOGGER.exception('error_once_only - Error Message: {}'.format(err))
    
    return JsonResponse(last_endpoint_metric)



class APISummaryPartialFunctionView(APIMetricsView):
    template_name = 'metrics/api_summary_partial_function.html'

    def get_context_data(self, **kwargs):
        context = super(APISummaryPartialFunctionView, self).get_context_data(
            **kwargs)
        barchart_data = json.dumps(get_barchart_data(
            context['metrics'], 'implemented_by_partial_function'))

        context.update({
            'barchart_data': barchart_data,
        })
        return context


class ConnectorMetricsView(MetricsView):
    """View for connector metrics"""
    form_class = ConnectorMetricsForm
    template_name = 'metrics/connector.html'
    api_urlpath = '/management/connector/metrics'

class MonthlyMetricsSummaryView(LoginRequiredMixin, TemplateView):
    """View for metrics summary (sort of abstract base class)"""
    form_class = MonthlyMetricsSummaryForm
    template_name = 'metrics/monthly_summary.html'
    api_urlpath = None

    def get_form(self):
        """
        Get bound form either from request.GET or initials
        We need a bound form because we already send a request to the API
        without user intervention on initial request
        """
        if self.request.GET:
            data = self.request.GET
        else:
            fields = self.form_class.declared_fields
            data = {}
            for name, field in fields.items():
                if field.initial:
                    data[name] = field.initial
        form = self.form_class(data)
        return form

    def to_django(self, metrics):
        """
        Convert metrics data from API to format understood by Django
        - Make datetime out of string in field 'date'
        """
        for metric in metrics:
            metric['date'] = datetime.datetime.strptime(
                metric['date'], API_DATE_FORMAT_WITH_MILLISECONDS)
        return metrics

    def to_api(self, cleaned_data):
        """
        Convert form data from Django to format understood by API
        - API treats empty parameters as actual values, so we have to remove
        them
        - Need to convert datetimes into required format
        """
        params = []
        for name, value in cleaned_data.items():
            # Maybe we should define the API format as Django format to not
            # have to convert in places like this?
            if value.__class__.__name__ == 'datetime':
                value = value.strftime(settings.API_DATE_FORMAT_WITH_MILLISECONDS)
            if value:
                # API does not like quoted data
                params.append('{}={}'.format(name, value))
        params = '&'.join(params)
        return params

    def get_app_name_parameters(self, include_app_names):
        #if len(app_names) == 1:
        #    return
        #1. Parse include_app_names create a list using a commo (,) separator
        #2. Trim each word (remove space),
        #3. Then is one word, &app_name = thing
        #4. IF IT IS MORE than one word then return number of app without space
        #5. return either &app_name=thing
        #6. Or
        #7. return &include_app_names=thing1,thing2,
        #8. url encode
        #app_names = []
        #input_string = "simon says, foo, bar , App 2 "
        input_string = include_app_names.strip()
        result = ""
        if input_string != "":
            input_list = input_string.strip().split(",")
            #print("input_list is:", input_list)
            cleaned_list = [item.strip() for item in input_list]
            #print("cleaned_list is: ", cleaned_list)
            cleaned_string=', '.join([str(item) for item in cleaned_list])
            #print("cleaned_string is:", cleaned_string)
            url_encoded_string = urllib.parse.quote(cleaned_string)
            #print("url_encoded_string is:", url_encoded_string)
            if len(cleaned_list) == 0:
                result = ""
            elif len(cleaned_list) == 1:
                result = "&app_name={}".format(url_encoded_string)
            else:
                result = "&include_app_names={}".format(url_encoded_string)
        return result
    def get_aggregate_metrics(self, from_date, to_date, include_app_names):
        """
        Gets the metrics from the API, using given parameters,
        There are different use cases, so we accept different parameters.
        only_show_api_explorer_metrics has the default value False, because it is just used for app = API_Explorer.
        """
        try:
            print("get_app_name_parameters is: ", self.get_app_name_parameters(include_app_names))
            api_calls_total = 0
            average_response_time = 0
            url_path = '/management/aggregate-metrics'
            #if only_show_api_explorer_metrics:
            #    urlpath = urlpath + '?from_date={}&to_date={}&app_name={}'.format(from_date, to_date)
            #elif (not only_show_api_explorer_metrics):
            #    urlpath = urlpath + '?from_date={}&to_date={}&exclude_implemented_by_partial_functions={}&exclude_url_pattern={}'.format(
            #        from_date, to_date, ",".join(local_settings.EXCLUDE_FUNCTIONS), ",".join(local_settings.EXCLUDE_URL_PATTERN))
            #
            #else:
            url_path =  url_path + '?from_date={}&to_date={}{}'.format(from_date, to_date, self.get_app_name_parameters(include_app_names))
            #print("get_app_name_parameters(include_app_names) is:", self.get_app_name_parameters(include_app_names))
            #print("url_path is: ", url_path)
            cache_key = get_cache_key_for_current_call(self.request, url_path)
            api_cache = None
            try:
                api_cache = cache.get(cache_key)
            except Exception as err:
                api_cache = None
            if not api_cache is None:
                metrics = api_cache
            else:
                api = API(self.request.session.get('obp'))
                metrics = api.get(url_path)
                api_cache = cache.set(cache_key, metrics)
                LOGGER.warning('{0}: {1}'.format(CACHE_SETTING_URL_MSG, url_path))
                LOGGER.warning('{0}: {1}'.format(CACHE_SETTING_KEY_MSG, cache_key))

            api_calls_total, average_calls_per_day, average_response_time = self.get_internal_api_call_metrics(
                api_calls_total, average_response_time, cache_key, from_date, metrics, to_date, url_path)
            return api_calls_total, average_response_time, int(average_calls_per_day)
        except APIError as err:
            error_once_only(self.request, err)
        except Exception as err:
            error_once_only(self.request, err)

    def get_internal_api_call_metrics(self, api_calls_total, average_response_time, cache_key, from_date, metrics,
                                      to_date, urlpath):
        api_calls_total = metrics[0]["count"]
        average_response_time = metrics[0]["average_response_time"]
        to_date = datetime.datetime.strptime(to_date, API_DATE_FORMAT_WITH_MILLISECONDS)
        from_date = datetime.datetime.strptime(from_date, API_DATE_FORMAT_WITH_MILLISECONDS)
        number_of_days = abs((to_date - from_date).days)
        # if number_of_days= 0, then it means calls_per_hour
        average_calls_per_day = api_calls_total if (number_of_days == 0) else api_calls_total / number_of_days
        return api_calls_total, average_calls_per_day, average_response_time

    def get_active_apps(self, from_date, to_date):
        """
         Gets the metrics from the API, using given parameters,
         """
        apps = []
        form = self.get_form()
        active_apps_list = []
        urlpath = '/management/metrics/top-consumers?from_date={}&to_date={}&exclude_implemented_by_partial_functions={}&exclude_url_pattern={}'.format(
            from_date, to_date, ",".join(EXCLUDE_FUNCTIONS), ",".join(EXCLUDE_URL_PATTERN))
        api = API(self.request.session.get('obp'))
        try:
            apps = api.get(urlpath)
            if apps is not None and 'code' in apps and apps['code']==403:
                error_once_only(self.request, apps['message'])
            else:
                active_apps_list = list(apps['top_consumers'])
        except APIError as err:
            error_once_only(self.request, err)
        except Exception as err:
            error_once_only(self.request, err)
        return active_apps_list


    def get_total_number_of_apps(self, cleaned_data, from_date, to_date):
        apps = []
        from_date = datetime.datetime.strptime(from_date, API_DATE_FORMAT_WITH_MILLISECONDS)
        to_date = datetime.datetime.strptime(to_date, API_DATE_FORMAT_WITH_MILLISECONDS)
        apps_list =  self.get_all_consumers()

        for app in apps_list:
            app_created_date = datetime.datetime.strptime(app["created"], API_DATE_FORMAT_WITH_SECONDS )

            if app_created_date < from_date and app_created_date > to_date:
                apps_list.remove(app)

        app_names = []

        for apps in apps_list:
            app_names.append(apps["app_name"])

        # If include OBP Apps is selected
        #if not cleaned_data.get('include_obp_apps'):
        #    for app in app_names:
        #        if app in local_settings.EXCLUDE_APPS:
        #            app_names.remove(app)

        app_names = list(filter(None, app_names))

        unique_app_names = list(set(app_names))

        developer_emails = []
        for apps in apps_list:
            developer_emails.append(apps["developer_email"])

        developer_emails = list(filter(None, developer_emails))
        unique_developer_emails = list(set(developer_emails))

        number_of_apps_with_unique_app_name = len(unique_app_names)
        number_of_apps_with_unique_developer_email = len(unique_developer_emails)

        return unique_app_names, number_of_apps_with_unique_app_name, number_of_apps_with_unique_developer_email

    def get_all_consumers(self):
        urlpath = '/management/consumers'
        api = API(self.request.session.get('obp'))
        cache_key = get_cache_key_for_current_call(self.request, urlpath)
        api_cache = None
        try:
            api_cache = cache.get(cache_key)
        except Exception as err:
            api_cache = None
        if api_cache is not None:
            apps_list = api_cache
        else:
            try:
                apps = api.get(urlpath)
                apps_list = apps["consumers"]
                cache.set(cache_key, apps_list, 60 * 60)  # for the consumers we cache for 1 hour, consumers may be increased
                LOGGER.warning('{0}: {1}'.format(CACHE_SETTING_URL_MSG, urlpath))
                LOGGER.warning('{0}: {1}'.format(CACHE_SETTING_KEY_MSG, cache_key))
            except APIError as err:
                error_once_only(self.request, err)
            except Exception as err:
                error_once_only(self.request, err)
        return apps_list

    def calls_per_delta(self, from_date_string, to_date_string, include_app_names, **delta ):
        """
        return how many calls were made in total per given delta.
        Here we need to convert date_string to datetime object, and calculate the dates.
        """

        # we need to convert string to datetime object, then we can calculate the date
        from_datetime_object = datetime.datetime.strptime(from_date_string, API_DATE_FORMAT_WITH_MILLISECONDS)
        to_datetime_object = datetime.datetime.strptime(to_date_string , API_DATE_FORMAT_WITH_MILLISECONDS)
        time_delta_in_loop = from_datetime_object + timedelta(**delta)

        result_list = []
        result_list_pure = []
        date_list = []
        #while time_delta_in_loop <= to_datetime_object:
        while time_delta_in_loop <= to_datetime_object + timedelta(days=1, hours=1):
            try:
                # here we need to first convert datetime object to String
                from_date= from_datetime_object.strftime(API_DATE_FORMAT_WITH_MILLISECONDS)
                to_date= time_delta_in_loop.strftime(API_DATE_FORMAT_WITH_MILLISECONDS)
                aggregate_metrics = self.get_aggregate_metrics(from_date, to_date, include_app_names)
                result = aggregate_metrics[0]
                result_list_pure.append(result)
                result_list.append('{} - {} # {}'.format(from_datetime_object, time_delta_in_loop, result))
                date_list.append(from_datetime_object)
            except Exception as err:
                error_once_only(self.request, err)
                break

            from_datetime_object = time_delta_in_loop
            time_delta_in_loop = time_delta_in_loop + timedelta(**delta)
            print("time_delta_in_loop in **delta is", time_delta_in_loop)

        return (result_list, result_list_pure, date_list)


    def calls_per_month(self,from_date, to_date, include_app_names):
        """
        Convenience function to print number of calls per month
        It is actually 30 days, not a month
        """
        calls_per_month_list, calls_per_month, month_list = self.calls_per_delta(from_date, to_date, include_app_names, days=30)
        return calls_per_month_list, calls_per_month, month_list


    def calls_per_day(self,from_date, to_date, include_app_names):
        """
        Convenience function to print number of calls per day
        """
        calls_per_day, calls_per_day_pure, date_list = self.calls_per_delta(from_date, to_date, include_app_names, days=1)

        if len(calls_per_day) >= 90:
            calls_per_day = calls_per_day[-90:]
            calls_per_day_pure = calls_per_day_pure[-90:]
            date_list = date_list[-90:]

        elif len(calls_per_day) >= 30:
            calls_per_day = calls_per_day[-30:]
            calls_per_day_pure = calls_per_day_pure[-30:]
            date_list = date_list[-30:]

        return calls_per_day, calls_per_day_pure, date_list

    def calls_per_half_day(self,from_date, include_app_names):
        """
        Convenience function to print number of calls per half day
        """
        return self.calls_per_delta(from_date, hours=12)


    def calls_per_hour(self,from_date, to_date, include_app_names):
        """
        Convenience function to print number of calls per hour
        """
        calls_per_hour_list, calls_per_hour, hour_list = self.calls_per_delta(from_date, to_date, include_app_names, hours=1)
        return calls_per_hour_list, calls_per_hour, hour_list

    def plot_line_chart(self, plot_data, date_month_list, period):
        date_list = []
        month_list = []
        hour_list = []

        if period == 'day':
            self._day(plot_data, date_month_list, date_list)

        elif period == 'month':
            self._month(plot_data, date_month_list, month_list)

        elif period == 'hour':
            self._hour(plot_data, date_month_list, hour_list)

        plt.xticks(rotation=90, fontsize=6)

        plt.ylabel("Number of API calls", fontsize=8)
        plt.tick_params(axis='y', labelsize=8)

        plt.ylim(ymin=0)
        plt.tight_layout()
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8').replace('\n', '')
        buf.close()
        # Clear the previous plot.
        plt.gcf().clear()
        return image_base64

    def _day(self, plot_data, date_month_list, date_list):
        if len(plot_data) == 0:
            plt.xlabel("Dates", fontsize=8)
            plt.plot()
        else:
            plt.title("API calls per day", fontsize=14)
            plt.xlabel("Dates", fontsize=8)
            for date in date_month_list:
                date = date.strftime('%B %d')
                date_list.append(str(date))
            plt.plot(date_list, plot_data, linewidth=1, marker='o')

    def _month(self, plot_data, date_month_list, month_list):
        if len(plot_data) == 0:
            plt.xlabel("Months", fontsize=8)
            plt.plot()
        else:
            plt.title("API calls per month", fontsize=14)
            plt.xlabel("Months", fontsize=8)
            for date in date_month_list:
                month = date.strftime('%B %Y')
                month_list.append(str(month))
            plt.plot(month_list, plot_data, linewidth=1, marker='o')

    def _hour(self, plot_data, date_month_list, hour_list):
        if len(plot_data) == 0:
            plt.xlabel("Hours", fontsize=8)
            plt.plot()
        else:
            plt.title("API calls per hour", fontsize=14)
            plt.xlabel("Hours", fontsize=8)
            for date in date_month_list:
                hour = date.strftime('%B %d -- %H : %m')
                hour_list.append(str(hour))
            plt.plot(hour_list, plot_data, linewidth=1, marker='o')

    def plot_bar_chart(self, data):
        x = []
        y = []
        for item in data:
            y.append(item['count'])
            x.append(item['Implemented_by_partial_function'])
        plt.barh(x, y)
        plt.title("Top apis", fontsize=10)
        plt.xlabel("Number of API Calls", fontsize=8)
        plt.xticks([])
        plt.ylabel("Partial function", fontsize=8)
        plt.tick_params(axis='y', labelsize=8)
        for i, j in zip(y, x):
            plt.text(i, j, str(i), clip_on=True, ha='center',va='center', fontsize=8)
        plt.tight_layout()
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8').replace('\n', '')
        buf.close()
        # Clear the previous plot.
        plt.gcf().clear()
        return image_base64

    def plot_topconsumer_bar_chart(self, data):
        x = []
        y = []
        for item in data:
            y.append(item['count'])
            x.append(item['app_name'])
        plt.barh(x, y)
        plt.title("Top consumers", fontsize=10)
        plt.xlabel("Number of API Calls", fontsize=8)
        plt.xticks([])
        plt.ylabel("Consumers", fontsize=8)
        plt.tick_params(axis='y', labelsize=8)
        for i, j in zip(y, x):
            plt.text(i, j, str(i), clip_on=True, ha='center',va='center', fontsize=8)
        plt.tight_layout()
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8').replace('\n', '')
        buf.close()
        # Clear the previous plot.
        plt.gcf().clear()
        return image_base64

    def get_users_cansearchwarehouse(self):
        users = []
        users_with_cansearchwarehouse = []
        email_with_cansearchwarehouse = []
        api = API(self.request.session.get('obp'))
        try:
            urlpath = '/users'
            users = api.get(urlpath)
            if users is not None and 'code' in users and users['code'] == 403:
                error_once_only(self.request, users['message'])
            if 'users' not in users:
                users['users']=[]
            else:
                self._update_user_with_cansearchwarehouse(users, users_with_cansearchwarehouse, email_with_cansearchwarehouse)
            # fail gracefully in case API provides new structure
        except APIError as err:
            error_once_only(self.request, err)
        except KeyError as err:
            messages.error(self.request, 'KeyError: {}'.format(err))
        except Exception as err:
            error_once_only(self.request, err)

        user_email_cansearchwarehouse = dict(zip(users_with_cansearchwarehouse, email_with_cansearchwarehouse))
        number_of_users_with_cansearchwarehouse = len(user_email_cansearchwarehouse)
        return user_email_cansearchwarehouse, number_of_users_with_cansearchwarehouse

    def _update_user_with_cansearchwarehouse(self, users, users_with_cansearchwarehouse, email_with_cansearchwarehouse):
        for user in users['users']:
            for entitlement in user['entitlements']['list']:
                if 'CanSearchWarehouse' in entitlement['role_name']:
                    users_with_cansearchwarehouse.append(user["username"])
                    email_with_cansearchwarehouse.append(user["email"])

    def _api_data(self, urlpath, data_key):
        api = API(self.request.session.get('obp'))
        data = []
        try:
            data = api.get(urlpath)
            if data is not None and 'code' in data and data['code']==403:
                error_once_only(self.request, data['message'])
                data=[]
            else:
                data = data[data_key]
        except APIError as err:
            error_once_only(self.request, err)
        except Exception as err:
            error_once_only(self.request, err)
        return data

    def get_top_apis(self, cleaned_data, from_date, to_date):
        top_apis = []
        urlpath = '/management/metrics/top-apis?limit=10&from_date={}&to_date={}&exclude_implemented_by_partial_functions={}&exclude_url_pattern={}'.format(
                from_date, to_date, ",".join(EXCLUDE_FUNCTIONS), ",".join(EXCLUDE_URL_PATTERN))
        top_apis = self._api_data(urlpath, 'top_apis')

        for api in top_apis:
            if api['Implemented_by_partial_function'] == "":
                top_apis.remove(api)

        for api in top_apis:
            api['Implemented_by_partial_function'] = api['Implemented_by_partial_function'] + '(' + api['implemented_in_version'] + ')'
        top_apis = top_apis[:10]
        top_apis = reversed(top_apis)
        return top_apis

    def get_top_consumers(self, cleaned_data, from_date, to_date):
        top_consumers = []
        urlpath = '/management/metrics/top-consumers?limit=10&from_date={}&to_date={}&exclude_implemented_by_partial_functions={}&exclude_url_pattern={}'.format(
                from_date, to_date, ",".join(EXCLUDE_FUNCTIONS), ",".join(EXCLUDE_URL_PATTERN))
        top_consumers = self._api_data(urlpath, 'top_consumers')

        for consumer in top_consumers:
            if consumer['app_name'] == "":
                top_consumers.remove(consumer)

        top_consumers = reversed(top_consumers)

        return top_consumers

    def get_top_warehouse_calls(self, cleaned_data, from_date, to_date):
        try:
            top_apis = self.get_top_apis(cleaned_data, from_date, to_date)
            top_warehouse_calls = []
            for api in top_apis:
                if "elasticSearchWarehouse" in api['Implemented_by_partial_function']:
                    top_warehouse_calls.append(api)
        except APIError as err:
            error_once_only(self.request, err)
        except Exception as err:
            error_once_only(self.request, err)
        return top_warehouse_calls

    def get_top_apps_using_warehouse(self, from_date, to_date):
        top_apps_using_warehouse = []

        urlpath = '/management/metrics/top-consumers?from_date={}&to_date={}&implemented_by_partial_function={}'.format(
            from_date, to_date, "elasticSearchWarehouse")
        api = API(self.request.session.get('obp'))
        try:
            top_apps_using_warehouse = api.get(urlpath)
            if top_apps_using_warehouse is not None and 'code' in top_apps_using_warehouse and top_apps_using_warehouse['code']==403:
                error_once_only(self.request, top_apps_using_warehouse['message'])
                top_apps_using_warehouse = []
            else:
                top_apps_using_warehouse = top_apps_using_warehouse["top_consumers"][:2]
        except APIError as err:
            error_once_only(self.request, err)
        except Exception as err:
            error_once_only(self.request, err)

        return top_apps_using_warehouse

    def median_time_to_first_api_call(self, from_date, to_date):
        return 0 #TODO this cost too much time, do not use this at the moment.
        form = self.get_form()
        form = self.get_form()
        new_apps_list = []
        apps = []
        apps_list = self.get_all_consumers()

        for app in apps_list:
            created_date = datetime.datetime.strptime(app['created'], '%Y-%m-%dT%H:%M:%SZ')
            created_date = created_date.strftime(API_DATE_FORMAT_WITH_MILLISECONDS)
            created_date = datetime.datetime.strptime(created_date, API_DATE_FORMAT_WITH_MILLISECONDS)
            if created_date >= datetime.datetime.strptime(from_date, API_DATE_FORMAT_WITH_MILLISECONDS):
                new_apps_list.append(app)

        times_to_first_call = []

        strfrom_date=datetime.datetime.strptime(from_date, API_DATE_FORMAT_WITH_MILLISECONDS)
        strto_date=datetime.datetime.strptime(to_date, API_DATE_FORMAT_WITH_MILLISECONDS)
        for app in new_apps_list:
            urlpath_metrics = '/management/metrics?from_date={}&to_date={}&consumer_id={}&sort_by={}&direction={}&limit={}'.format(
                from_date, to_date, app['consumer_id'], 'date', 'asc', '1')
            cache_key = get_cache_key_for_current_call(self.request, urlpath_metrics)
            api = API(self.request.session.get('obp'))
            try:
                api_cache=None
                try:
                    api_cache=cache.get(cache_key)
                except Exception as err:
                    api_cache=None
                metrics=[]
                if not api_cache is None:
                    metrics=api_cache
                else:
                    metrics = api.get(urlpath_metrics)

                    if metrics is not None and 'code' in metrics and metrics['code'] == 403:
                        error_once_only(self.request, metrics['message'])
                        if(metrics['message'].startswith('OBP-20006')):
                            break
                        metrics = []
                    else:
                        metrics = list(metrics['metrics'])
                        cache.set(cache_key, metrics)
                        LOGGER.warning('The cache is setting, url is: {}'.format(urlpath_metrics))
                        LOGGER.warning('The cache is setting key is: {}'.format(cache_key))
                if metrics:
                    time_difference = datetime.datetime.strptime(metrics[0]['date'], '%Y-%m-%dT%H:%M:%S.%fZ') - datetime.datetime.strptime(app['created'], '%Y-%m-%dT%H:%M:%SZ')
                    times_to_first_call.append(time_difference.total_seconds())


            except APIError as err:
                error_once_only(self.request, err)
            except Exception as err:
                error_once_only(self.request, 'Unknown Error. {}'.format(err))

        if times_to_first_call:
            median = statistics.median(times_to_first_call)
            delta = datetime.timedelta(seconds=median)
        else:
            delta = 0

        return delta

    def get_context_data(self, **kwargs): return self.prepare_general_context(SummaryType.MONTHLY)

    def prepare_general_context(self, web_page_type,  **kwargs):
        try:
            form = self.get_form()
            print("form from get_form", form)
            per_day_chart=[]
            calls_per_month_list=[]
            per_month_chart=[]
            calls_per_hour_list=[]
            per_hour_chart=[]
            if form.is_valid():
                # = form.cleaned_data.get('include_obp_apps')
                include_app_names = form.cleaned_data.get("include_app_names")
                #if exclude_app_names not in local_settings.EXCLUDE_APPS:
                #    error_once_only(self.request, "Invalid Exclude App Name, Please select" + str(local_settings.EXCLUDE_APPS) + "Anyone of these")
                form_to_date_string = form.data['to_date']
                print(form.data, "Form data")
                to_date = convert_form_date_to_obpapi_datetime_format(form_to_date_string)
                print("to_date", to_date)
                if (web_page_type == SummaryType.DAILY):
                    # for one day, the from_date is 1 day ago.
                    from_date = return_to_days_ago(to_date, 0)
                    calls_per_hour_list, calls_per_hour, hour_list = self.calls_per_hour(from_date, to_date, include_app_names)
                    per_hour_chart = self.plot_line_chart(calls_per_hour, hour_list, 'hour')

                if (web_page_type == SummaryType.WEEKLY):
                    # for one month, the from_date is 7 days ago.
                    from_date = return_to_days_ago(to_date, 7)
                    calls_per_day_list, calls_per_day, date_list = self.calls_per_day(from_date, to_date, include_app_names)
                    per_day_chart = self.plot_line_chart(calls_per_day, date_list, "day")

                if (web_page_type == SummaryType.MONTHLY):
                    # for one month, the from_date is 30 days ago.
                    from_date = return_to_days_ago(to_date, 30)
                    calls_per_day_list, calls_per_day, date_list = self.calls_per_day(from_date, to_date, include_app_names)
                    per_day_chart = self.plot_line_chart(calls_per_day, date_list, "day")

                if (web_page_type == SummaryType.QUARTERLY):
                    # for one quarter, the from_date is 90 days ago.
                    from_date = (datetime.datetime.strptime(to_date, API_DATE_FORMAT_WITH_MILLISECONDS) - timedelta(90)).strftime(API_DATE_FORMAT_WITH_MILLISECONDS)
                    calls_per_month_list, calls_per_month, month_list = self.calls_per_month(from_date, to_date, include_app_names)
                    per_month_chart = self.plot_line_chart(calls_per_month, month_list, 'month')

                if (web_page_type == SummaryType.YEARLY):
                    from_date = return_to_days_ago(to_date, 365)
                    #calls_per_month_list, calls_per_month, month_list = self.calls_per_month(, from_date, to_date)
                    calls_per_month_list, calls_per_month, month_list = self.calls_per_month(from_date, to_date, include_app_names)
                    per_month_chart = self.plot_line_chart(calls_per_month, month_list, "month")

                if (web_page_type == SummaryType.CUSTOM):
                    # for one month, the from_date is x day ago.
                    form_from_date_string = form.data['from_date_custom']
                    from_date = convert_form_date_to_obpapi_datetime_format(form_from_date_string)
                    calls_per_day_list, calls_per_day, date_list = self.calls_per_day(from_date, to_date, include_app_names)
                    if (len(calls_per_day) <= 31):
                        per_day_chart = self.plot_line_chart(calls_per_day, date_list, "day")
                    else:
                        per_day_chart = self.plot_line_chart(calls_per_day, date_list, "month")

                api_host_name = API_HOST
                top_apps_using_warehouse = self.get_top_apps_using_warehouse(from_date, to_date)
                user_email_cansearchwarehouse, number_of_users_with_cansearchwarehouse = self.get_users_cansearchwarehouse()
                median_time_to_first_api_call = self.median_time_to_first_api_call(from_date, to_date)

                top_apis = self.get_top_apis(form.cleaned_data, from_date, to_date)
                top_apis_bar_chart = self.plot_bar_chart(top_apis)
                top_consumers = self.get_top_consumers(form.cleaned_data, from_date, to_date)
                top_consumers_bar_chart = self.plot_topconsumer_bar_chart(top_consumers)
                top_warehouse_calls = self.get_top_warehouse_calls(form.cleaned_data, from_date, to_date)
                api_calls, average_response_time, average_calls_per_day = self.get_aggregate_metrics(from_date, to_date, include_app_names)
                unique_app_names, number_of_apps_with_unique_app_name, number_of_apps_with_unique_developer_email = self.get_total_number_of_apps(
                    form.cleaned_data, from_date, to_date)
                active_apps_list = self.get_active_apps(from_date, to_date)

                context = super(MonthlyMetricsSummaryView, self).get_context_data(**kwargs)
                context.update({
                    'form': form,
                    'api_calls': api_calls,
                    'include_app_names': include_app_names,
                    'calls_per_month_list': calls_per_month_list,
                    'per_month_chart': per_month_chart,
                    'per_day_chart': per_day_chart,
                    'calls_per_hour_list': calls_per_hour_list,
                    'per_hour_chart': per_hour_chart,
                    'number_of_apps_with_unique_app_name': number_of_apps_with_unique_app_name,
                    'number_of_apps_with_unique_developer_email': number_of_apps_with_unique_developer_email,
                    'active_apps_list': active_apps_list,
                    'average_calls_per_day': average_calls_per_day,
                    'average_response_time': average_response_time,
                    'top_warehouse_calls': top_warehouse_calls,
                    'top_apps_using_warehouse': top_apps_using_warehouse,
                    'user_email_cansearchwarehouse': user_email_cansearchwarehouse,
                    'number_of_users_with_cansearchwarehouse': number_of_users_with_cansearchwarehouse,
                    'api_host_name': api_host_name,
                    'from_date': (datetime.datetime.strptime(from_date, API_DATE_FORMAT_WITH_MILLISECONDS)).strftime('%d %B %Y'),
                    'to_date': (datetime.datetime.strptime(to_date, API_DATE_FORMAT_WITH_MILLISECONDS)).strftime('%d %B %Y'),
                    'top_apis': top_apis,
                    'top_apis_bar_chart': top_apis_bar_chart,
                    'top_consumers_bar_chart': top_consumers_bar_chart,
                    'median_time_to_first_api_call': median_time_to_first_api_call,
                    #'excluded_apps':[exclude_app_names if exclude_app_names in local_settings.EXCLUDE_APPS else "null"],
                })
                return context
            else:
                error_once_only(self.request, str(form.errors))
        except Exception as err:
            error_once_only(self.request, err)
    def _daily_and_weekly(self, web_page_type,to_date, per_hour_chart, per_day_chart, from_date):
        if (web_page_type == SummaryType.DAILY):
            # for one day, the from_date is 1 day ago.
            from_date = return_to_days_ago(to_date, 1)
            calls_per_hour_list, calls_per_hour, hour_list = self.calls_per_hour(from_date, to_date, include_app_names)
            per_hour_chart = self.plot_line_chart(calls_per_hour, hour_list, 'hour')

        if (web_page_type == SummaryType.WEEKLY):
            # for one month, the from_date is 7 days ago.
            from_date = return_to_days_ago(to_date, 7)
            calls_per_day_list, calls_per_day, date_list = self.calls_per_day(from_date, to_date, include_app_names)
            per_day_chart = self.plot_line_chart(calls_per_day, date_list, "day")

        return (from_date, per_hour_chart, per_day_chart)

    def _monthly_and_quarterly(self, web_page_type,to_date, per_day_chart, per_month_chart, from_date):
        if (web_page_type == SummaryType.MONTHLY):
            # for one month, the from_date is 30 days ago.
            from_date = return_to_days_ago(to_date, 30)
            calls_per_day_list, calls_per_day, date_list = self.calls_per_day(from_date, to_date, include_app_names)
            per_day_chart = self.plot_line_chart(calls_per_day, date_list, "day")

        if (web_page_type == SummaryType.QUARTERLY):
            # for one quarter, the from_date is 90 days ago.
            from_date = (datetime.datetime.strptime(to_date, API_DATE_FORMAT_WITH_MILLISECONDS) - timedelta(90)).strftime(API_DATE_FORMAT_WITH_MILLISECONDS)
            calls_per_month_list, calls_per_month, month_list = self.calls_per_month(from_date, to_date, include_app_names)
            per_month_chart = self.plot_line_chart(calls_per_month, month_list, 'month')

        return (from_date, per_day_chart, per_month_chart)

    def _yearly_and_custom(self, web_page_type,to_date, per_month_chart, per_day_chart, from_date):
        if (web_page_type == SummaryType.YEARLY):
            from_date = return_to_days_ago(to_date, 365)
            calls_per_month_list, calls_per_month, month_list = self.calls_per_month(from_date, to_date, include_app_names)
            per_month_chart = self.plot_line_chart(calls_per_month, month_list, "month")

        if (web_page_type == SummaryType.CUSTOM):
            # for one month, the from_date is x day ago.
            form_from_date_string = form.data['from_date_custom']
            from_date = convert_form_date_to_obpapi_datetime_format(form_from_date_string)
            calls_per_day_list, calls_per_day, date_list = self.calls_per_day(from_date, to_date, include_app_names)
            per_day_chart = self.plot_line_chart(calls_per_day, date_list, "day")

        return (from_date, per_month_chart, per_day_chart)

class YearlySummaryView(MonthlyMetricsSummaryView):
    template_name = 'metrics/yearly_summary.html'
    def get_context_data(self, **kwargs): return self.prepare_general_context(SummaryType.YEARLY, **kwargs)

class QuarterlySummaryView(MonthlyMetricsSummaryView):
    template_name = 'metrics/quarterly_summary.html'
    def get_context_data(self, **kwargs): return self.prepare_general_context(SummaryType.QUARTERLY, **kwargs)


class WeeklySummaryView(MonthlyMetricsSummaryView):
    template_name = 'metrics/weekly_summary.html'
    def get_context_data(self, **kwargs): return self.prepare_general_context(SummaryType.WEEKLY, **kwargs)

class DailySummaryView(MonthlyMetricsSummaryView):
    template_name = 'metrics/daily_summary.html'
    def get_context_data(self, **kwargs): return self.prepare_general_context(SummaryType.DAILY, **kwargs)

class HourlySummaryView(MonthlyMetricsSummaryView):
    template_name = 'metrics/hourly_summary.html'

class CustomSummaryView(MonthlyMetricsSummaryView):
    form_class = CustomSummaryForm
    template_name = 'metrics/custom_summary.html'
    def get_context_data(self, **kwargs): return self.prepare_general_context(SummaryType.CUSTOM, **kwargs)