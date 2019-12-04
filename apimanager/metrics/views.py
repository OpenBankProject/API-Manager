# -*- coding: utf-8 -*-
"""
Views of metrics app
"""

import json
import hashlib
import operator
from datetime import datetime, timedelta

from django.conf import settings
from apimanager.settings import API_HOST, EXCLUDE_APPS, EXCLUDE_FUNCTIONS, EXCLUDE_URL_PATTERN, API_EXPLORER_APP_NAME, API_DATEFORMAT,CACHE_DATEFORMAT
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from obp.api import API, APIError
from .forms import APIMetricsForm, ConnectorMetricsForm, MetricsSummaryForm, CustomSummaryForm
from pylab import *
from django.core.cache import cache
import traceback
try:
    # Python 2
    import cStringIO
except ImportError:
    # Python 3
    import io
from io import BytesIO
import base64
import matplotlib.pyplot as plt
import statistics


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
                metric['date'], '%Y-%m-%dT%H:%M:%S.%fZ')
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
                value = value.strftime(settings.API_DATEFORMAT)
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
            metrics = api.get(urlpath)
            metrics = self.to_django(metrics['metrics'])
        except APIError as err:
            error_once_only(self.request, err)
        except KeyError as err:
            error_once_only(self.request, metrics['message'])
        except Exception as err:
            error_once_only(self.request, 'Unknown Error. {}'.format(type(err).__name__))
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

class MetricsSummaryView(LoginRequiredMixin, TemplateView):
    """View for metrics summary (sort of abstract base class)"""
    form_class = MetricsSummaryForm
    template_name = 'metrics/summary.html'
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
                metric['date'], API_DATEFORMAT)
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
                value = value.strftime(settings.API_DATEFORMAT)
            if value:
                # API does not like quoted data
                params.append('{}={}'.format(name, value))
        params = '&'.join(params)
        return params


    def get_aggregate_metrics(self, cleaned_data, from_date, to_date):
        """
        Gets the metrics from the API, using given cleaned form data.
        """
        form = self.get_form()
        metrics = []
        api_calls_total = 0
        average_response_time = 0

        # If Include OBP Apps is selected
        if cleaned_data.get('include_obp_apps'):
            urlpath = '/management/aggregate-metrics?from_date={}&to_date={}'.format(from_date, to_date)
            api = API(self.request.session.get('obp'))
            try:
                metrics = api.get(urlpath)
                if metrics is not None and 'code' in metrics and metrics['code']==403:
                    error_once_only(self.request, metrics['message'])
                # metrics = self.to_django(metrics)
                else:
                    api_calls_total = metrics[0]["count"]
                    average_response_time = metrics[0]["average_response_time"]
            except APIError as err:
                error_once_only(self.request, err)
            except Exception as err:
                error_once_only(self.request, 'Unknown Error. {}'.format(type(err).__name__))

        else:
            urlpath = '/management/aggregate-metrics?from_date={}&to_date={}&exclude_app_names={}&exclude_implemented_by_partial_functions={}&exclude_url_pattern={}'.format(
                from_date, to_date, ",".join(EXCLUDE_APPS),
                ",".join(EXCLUDE_FUNCTIONS), ",".join(EXCLUDE_URL_PATTERN))
            api = API(self.request.session.get('obp'))
            try:
                metrics = api.get(urlpath)
                if metrics is not None and 'code' in metrics and metrics['code']==403:
                    error_once_only(self.request, metrics['message'])
                # metrics = self.to_django(metrics)
                else:
                    api_calls_total = metrics[0]["count"]
                    average_response_time = metrics[0]["average_response_time"]
            except APIError as err:
                error_once_only(self.request, err)
            except Exception as err:
                error_once_only(self.request, 'Unknown Error. {}'.format(type(err).__name__))


        to_date = datetime.datetime.strptime(to_date, API_DATEFORMAT)
        from_date = datetime.datetime.strptime(from_date, API_DATEFORMAT)
        number_of_days = abs((to_date - from_date).days)
        average_calls_per_day = api_calls_total / number_of_days

        return api_calls_total, average_response_time, int(average_calls_per_day)

    def get_aggregate_metrics_api_explorer(self, from_date, to_date):
        """
        Gets the metrics from the API, using given cleaned form data.
        """
        form = self.get_form()
        metrics = []
        api_calls_total = 0
        average_response_time = 0

        urlpath = '/management/aggregate-metrics?from_date={}&to_date={}&app_name={}'.format(from_date, to_date, API_EXPLORER_APP_NAME)
        api = API(self.request.session.get('obp'))
        try:
            metrics = api.get(urlpath)
            if metrics is not None and 'code' in metrics and metrics['code']==403:
                    error_once_only(self.request, metrics['message'])
            else:
                api_calls_total = metrics[0]["count"]
                average_response_time = metrics[0]["average_response_time"]
        except APIError as err:
            error_once_only(self.request, err)
        except Exception as err:
            error_once_only(self.request, "Unknown Error. {}".format(type(err).__name__))

        to_date = datetime.datetime.strptime(to_date, API_DATEFORMAT)
        from_date = datetime.datetime.strptime(from_date, API_DATEFORMAT)
        number_of_days = abs((to_date - from_date).days)
        average_calls_per_day = api_calls_total / number_of_days

        return api_calls_total, average_response_time, int(average_calls_per_day)

    def get_active_apps(self, cleaned_data, from_date, to_date):
        apps = []
        form = self.get_form()
        active_apps_list = []
        if cleaned_data.get('include_obp_apps'):
            urlpath = '/management/metrics/top-consumers?from_date={}&to_date={}'.format(from_date, to_date)
            api = API(self.request.session.get('obp'))
            try:
                apps = api.get(urlpath)
                if apps is not None and 'code' in apps and apps['code']==403:
                    error_once_only(self.request, apps['message'])
                else:
                    active_apps_list = list(apps)
            except APIError as err:
                error_once_only(self.request, err)
            except Exception as err:
                error_once_only(self.request, 'Unknown Error. {}'.format(type(err).__name__))
        else:
            urlpath = '/management/metrics/top-consumers?from_date={}&to_date={}&exclude_app_names={}&exclude_implemented_by_partial_functions={}&exclude_url_pattern={}'.format(
                from_date, to_date, ",".join(EXCLUDE_APPS), ",".join(EXCLUDE_FUNCTIONS), ",".join(EXCLUDE_URL_PATTERN))
            api = API(self.request.session.get('obp'))
            try:
                apps = api.get(urlpath)
                if apps is not None and 'code' in apps and apps['code']==403:
                    error_once_only(self.request, apps['message'])
                else:
                    active_apps_list = list(apps)
            except APIError as err:
                error_once_only(self.request, err)
            except Exception as err:
                error_once_only(self.request, 'Unknown Error. {}'.format(type(err).__name__))

        return active_apps_list


    def get_total_number_of_apps(self, cleaned_data, from_date, to_date):
        apps = []
        apps_list = []
        from_date = datetime.datetime.strptime(from_date, API_DATEFORMAT)
        to_date = datetime.datetime.strptime(to_date, API_DATEFORMAT)
        urlpath='/management/consumers'
        api = API(self.request.session.get('obp'))
        try:
            apps = api.get(urlpath)
            if apps is not None and 'code' in apps and apps['code'] == 403:
                error_once_only(self.request, apps['message'])
            else:
                apps_list = apps["consumers"]
        except APIError as err:
            error_once_only(self.request, err)
        except Exception as err:
            error_once_only(self.request, 'Unknown Error. {}'.format(type(err).__name__))

        for app in apps_list:
            app_created_date = datetime.datetime.strptime(app["created"], '%Y-%m-%dT%H:%M:%SZ')

            if app_created_date < from_date and app_created_date > to_date:
                apps_list.remove(app)

        app_names = []

        for apps in apps_list:
            app_names.append(apps["app_name"])

        # If include OBP Apps is selected
        if cleaned_data.get('include_obp_apps'):
            app_names = app_names
        else:
            for app in app_names:
                if app in EXCLUDE_APPS:
                    app_names.remove(app)

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

    def calls_per_delta(self, cleaned_data, from_date, to_date, **delta ):
        """
        Prints how many calls were made in total per given delta
        """
        form = self.get_form()
        to_date = datetime.datetime.strptime(to_date, API_DATEFORMAT)

        from_date = datetime.datetime.strptime(from_date, API_DATEFORMAT)

        date_from = from_date
        date_to = from_date + timedelta(**delta)

        sum = 0
        metrics = []
        result_list = []
        result_list_pure = []
        date_list = []
        date_list.append(date_from)

        # If include_obp_apps is selected
        if cleaned_data.get('include_obp_apps'):
            while date_to <= to_date:
                urlpath = '/management/aggregate-metrics?from_date={}&to_date={}'.format(
                    date_from.strftime(API_DATEFORMAT), date_to.strftime(API_DATEFORMAT))
                apicaches=None
                try:
                    apicaches=cache.get('aggregate-metrics,{},{},{}'.format(self.request.session.get('obp')['authenticator_kwargs']['token'],date_from.strftime(CACHE_DATEFORMAT), date_to.strftime(CACHE_DATEFORMAT)))
                except Exception as err:
                    apicaches=None
                if apicaches:
                    result = apicaches
                    result_list_pure.append(result)
                    result_list.append('{} - {} # {}'.format(date_from, date_to, result))
                    sum += result
                else:
                    api = API(self.request.session.get('obp'))
                    try:
                        metrics = api.get(urlpath)
                        if metrics is not None and 'code' in metrics and metrics['code'] == 403:
                            error_once_only(self.request, metrics['message'])
                        else:
                            result = metrics[0]["count"]
                            result_list_pure.append(result)
                            result_list.append('{} - {} # {}'.format(date_from, date_to, result))
                            sum += result
                            
                            cache.set('aggregate-metrics,{},{},{}'.format(self.request.session.get('obp')['authenticator_kwargs']['token'],date_from.strftime(CACHE_DATEFORMAT), date_to.strftime(CACHE_DATEFORMAT)),result)
                    except APIError as err:
                        error_once_only(self.request, err)
                    except Exception as err:
                        error_once_only(self.request, 'Unknown Error. {}'.format(type(err).__name__))

                date_from = date_to
                date_list.append(date_from)
                date_to = date_to + timedelta(**delta)
        else:
            while date_to <= to_date:
                urlpath = '/management/aggregate-metrics?from_date={}&to_date={}&exclude_app_names={}'.format(
                    date_from.strftime(API_DATEFORMAT), date_to.strftime(API_DATEFORMAT), ",".join(EXCLUDE_APPS))
                apicaches=None
                try:
                    apicaches=cache.get('aggregate-metrics,{},{},{},{}'.format(self.request.session.get('obp')['authenticator_kwargs']['token'],date_from.strftime(CACHE_DATEFORMAT), date_to.strftime(CACHE_DATEFORMAT),",".join(EXCLUDE_APPS)))
                except Exception as err:
                    apicaches=None
                if apicaches:
                    result = apicaches
                    result_list_pure.append(result)
                    result_list.append('{} - {} # {}'.format(date_from, date_to, result))
                    sum += result
                else:
                    api = API(self.request.session.get('obp'))
                    try:
                        metrics = api.get(urlpath)
                        if metrics is not None and 'code' in metrics and metrics['code'] == 403:
                            error_once_only(self.request, metrics['message'])
                        else:
                            result = metrics[0]["count"]
                            result_list_pure.append(result)
                            result_list.append('{} - {} # {}'.format(date_from, date_to, result))
                            sum += result
                            
                            cache.set('aggregate-metrics,{},{},{},{}'.format(self.request.session.get('obp')['authenticator_kwargs']['token'],date_from.strftime(CACHE_DATEFORMAT), date_to.strftime(CACHE_DATEFORMAT),",".join(EXCLUDE_APPS)),result)
                    except APIError as err:
                        error_once_only(self.request, err)
                    except Exception as err:
                        error_once_only(self.request, 'Unknown Error. {}'.format(type(err).__name__))

                date_from = date_to
                date_list.append(date_from)
                date_to = date_to + timedelta(**delta)
        return result_list, result_list_pure, date_list


    def calls_per_month(self, cleaned_data, from_date, to_date):
        """
        Convenience function to print number of calls per month
        It is actually 30 days, not a month
        """
        calls_per_month_list, calls_per_month, month_list = self.calls_per_delta(cleaned_data, from_date, to_date, days=30)
        return calls_per_month_list, calls_per_month, month_list


    def calls_per_day(self, cleaned_data, from_date, to_date):
        """
        Convenience function to print number of calls per day
        """
        index = []
        calls_per_day, calls_per_day_pure, date_list = self.calls_per_delta(cleaned_data, from_date, to_date, days=1)

        if len(calls_per_day) >= 90:
            calls_per_day = calls_per_day[-90:]
            calls_per_day_pure = calls_per_day_pure[-90:]
            date_list = date_list[-90:]

        elif len(calls_per_day) >= 30:
            calls_per_day = calls_per_day[-30:]
            calls_per_day_pure = calls_per_day_pure[-30:]
            date_list = date_list[-30:]

        return calls_per_day, calls_per_day_pure, date_list

    def calls_per_half_day(self, cleaned_data, from_date):
        """
        Convenience function to print number of calls per half day
        """
        return self.calls_per_delta(cleaned_data, from_date, hours=12)


    def calls_per_hour(self, cleaned_data, from_date, to_date):
        """
        Convenience function to print number of calls per hour
        """
        calls_per_hour_list, calls_per_hour, hour_list = self.calls_per_delta(cleaned_data, from_date, to_date, hours=1)
        return calls_per_hour_list, calls_per_hour, hour_list

    def plot_line_chart(self, plot_data, date_month_list, period):
        date_list = []
        month_list = []
        hour_list = []

        if period == 'day':
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

        elif period == 'month':
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

        elif period == 'hour':
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

        plt.xticks(rotation=90, fontsize=6)

        plt.ylabel("Number of API calls", fontsize=8)
        plt.tick_params(axis='y', labelsize=8)

        plt.ylim(ymin=0)
        plt.tight_layout()
        buf = BytesIO()
        plt.savefig(buf, format='png')
        image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8').replace('\n', '')
        buf.close()
        # Clear the previous plot.
        plt.gcf().clear()
        return image_base64



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
        buf = BytesIO()
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
        except APIError as err:
            error_once_only(self.request, err)
        except Exception as err:
            error_once_only(self.request, 'Unknown Error. {}'.format(type(err).__name__))

        else:
            try:
                for user in users['users']:
                    for entitlement in user['entitlements']['list']:
                        if 'CanSearchWarehouse' in entitlement['role_name']:
                            users_with_cansearchwarehouse.append(user["username"])
                            email_with_cansearchwarehouse.append(user["email"])
            # fail gracefully in case API provides new structure
            except KeyError as err:
                messages.error(self.request, 'KeyError: {}'.format(err))
            except Exception as err:
                error_once_only(self.request, 'Unknown Error. {}'.format(type(err).__name__))

        user_email_cansearchwarehouse = dict(zip(users_with_cansearchwarehouse, email_with_cansearchwarehouse))
        number_of_users_with_cansearchwarehouse = len(user_email_cansearchwarehouse)
        return user_email_cansearchwarehouse, number_of_users_with_cansearchwarehouse

    def get_top_apis(self, cleaned_data, from_date, to_date):
        top_apis = []
        form = self.get_form()
        if cleaned_data.get('include_obp_apps'):
            urlpath = '/management/metrics/top-apis?from_date={}&to_date={}'.format(from_date, to_date)
            api = API(self.request.session.get('obp'))
            try:
                top_apis = api.get(urlpath)
                if top_apis is not None and 'code' in top_apis and top_apis['code']==403:
                    error_once_only(self.request, top_apis['message'])
                    top_apis=[]
                else:
                    top_apis = top_apis['top_apis']
            except APIError as err:
                error_once_only(self.request, err)
            except Exception as err:
                error_once_only(self.request, 'Unknown Error. {}'.format(type(err).__name__))
        else:
            urlpath = '/management/metrics/top-apis?from_date={}&to_date={}&exclude_app_names={}&exclude_implemented_by_partial_functions={}&exclude_url_pattern={}'.format(
                from_date, to_date, ",".join(EXCLUDE_APPS), ",".join(EXCLUDE_FUNCTIONS), ",".join(EXCLUDE_URL_PATTERN))
            api = API(self.request.session.get('obp'))
            try:
                top_apis = api.get(urlpath)
                if top_apis is not None and 'code' in top_apis and top_apis['code']==403:
                    error_once_only(self.request, top_apis['message'])
                    top_apis=[]
                else:
                    top_apis = top_apis['top_apis']
            except APIError as err:
                error_once_only(self.request, err)
            except Exception as err:
                error_once_only(self.request, 'Unknown Error. {}'.format(type(err).__name__))

        for api in top_apis:
            if api['Implemented_by_partial_function'] == "":
                top_apis.remove(api)

        for api in top_apis:
            api['Implemented_by_partial_function'] = api['Implemented_by_partial_function'] + '(' + api['implemented_in_version'] + ')'
        top_apis = top_apis[:10]
        top_apis = reversed(top_apis)

        return top_apis

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
            error_once_only(self.request, 'Unknown Error. {}'.format(type(err).__name__))
        return top_warehouse_calls

    def get_top_apps_using_warehouse(self, from_date, to_date):
        form = self.get_form()
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
            error_once_only(self.request, 'Unknown Error. {}'.format(type(err).__name__))

        return top_apps_using_warehouse

    def median_time_to_first_api_call(self, from_date, to_date):
        form = self.get_form()
        new_apps_list = []
        apps = []
        apps_list = []

        urlpath_consumers = '/management/consumers'
        apicaches=None
        try:
            apicaches=cache.get('consumers,{}'.format(self.request.session.get('obp')['authenticator_kwargs']['token']))
        except Exception as err:
            apicaches=None
        if apicaches:
            apps_list=apicaches
        else:
            api = API(self.request.session.get('obp'))
            try:
                apps = api.get(urlpath_consumers)
                if apps is not None and 'code' in apps and apps['code']==403:
                    error_once_only(self.request, apps['message'])
                else:
                    apps_list = apps["consumers"]
                    cache.set('consumers,{}'.format(self.request.session.get('obp')['authenticator_kwargs']['token']),apps_list)
            except APIError as err:
                error_once_only(self.request, err)
            except Exception as err:
                error_once_only(self.request, 'Unknown Error. {}'.format(type(err).__name__))

        for app in apps_list:
            created_date = datetime.datetime.strptime(app['created'], '%Y-%m-%dT%H:%M:%SZ')
            created_date = created_date.strftime(API_DATEFORMAT)
            created_date = datetime.datetime.strptime(created_date, API_DATEFORMAT)
            if created_date >= datetime.datetime.strptime(from_date, API_DATEFORMAT):
                new_apps_list.append(app)

        times_to_first_call = []

        strfrom_date=datetime.datetime.strptime(from_date, API_DATEFORMAT)
        strto_date=datetime.datetime.strptime(to_date, API_DATEFORMAT)
        for app in new_apps_list:
            urlpath_metrics = '/management/metrics?from_date={}&to_date={}&consumer_id={}&sort_by={}&direction={}&limit={}'.format(
                from_date, to_date, app['consumer_id'], 'date', 'asc', '1')
            api = API(self.request.session.get('obp'))
            try:
                apicaches=None
                try:
                    apicaches=cache.get('metrics,{},{},{},{}'.format(self.request.session.get('obp')['authenticator_kwargs']['token'],app['consumer_id'],strfrom_date.strftime(CACHE_DATEFORMAT), strto_date.strftime(CACHE_DATEFORMAT)))
                except Exception as err:
                    apicaches=None
                metrics=[]
                if apicaches :
                    metrics=apicaches
                else:
                    metrics = api.get(urlpath_metrics)
                    
                    if metrics is not None and 'code' in metrics and metrics['code'] == 403:
                        error_once_only(self.request, metrics['message'])
                        metrics = []
                    else:
                        metrics = list(metrics['metrics'])
                        cache.set('metrics,{},{},{},{}'.format(self.request.session.get('obp')['authenticator_kwargs']['token'],app['consumer_id'],strfrom_date.strftime(CACHE_DATEFORMAT), strto_date.strftime(CACHE_DATEFORMAT)),metrics)
                if metrics:
                    time_difference = datetime.datetime.strptime(metrics[0]['date'], '%Y-%m-%dT%H:%M:%S.%fZ') - datetime.datetime.strptime(app['created'], '%Y-%m-%dT%H:%M:%SZ')
                    times_to_first_call.append(time_difference.total_seconds())


            except APIError as err:
                error_once_only(self.request, err)
            except Exception as err:
                error_once_only(self.request, 'Unknown Error. {}'.format(type(err).__name__))

        if times_to_first_call:
            median = statistics.median(times_to_first_call)
            delta = datetime.timedelta(seconds=median)
        else:
            delta = 0

        return delta

    def get_context_data(self, **kwargs):
        form = self.get_form()

        to_date = datetime.datetime.strptime(form.data['to_date'], '%Y-%m-%d %H:%M:%S')
        to_date = to_date.strftime(API_DATEFORMAT)

        from_date = (datetime.datetime.strptime(to_date, API_DATEFORMAT) - timedelta(30)).strftime(API_DATEFORMAT)
        context = super(MetricsSummaryView, self).get_context_data(**kwargs)
        api_host_name = API_HOST
        top_apps_using_warehouse = self.get_top_apps_using_warehouse(from_date, to_date)
        user_email_cansearchwarehouse, number_of_users_with_cansearchwarehouse = self.get_users_cansearchwarehouse()
        median_time_to_first_api_call = self.median_time_to_first_api_call(from_date, to_date)
        if form.is_valid():
            top_apis = self.get_top_apis(form.cleaned_data, from_date, to_date)
            top_apis_bar_chart = self.plot_bar_chart(top_apis)
            top_warehouse_calls = self.get_top_warehouse_calls(form.cleaned_data, from_date, to_date)
            api_calls, average_response_time, average_calls_per_day = self.get_aggregate_metrics(form.cleaned_data, from_date, to_date)
            calls_by_api_explorer, average_response_time_api_explorer, average_calls_per_day_api_explorer = self.get_aggregate_metrics_api_explorer(from_date, to_date)
            calls_per_month_list, calls_per_month, date_list = self.calls_per_month(form.cleaned_data, from_date, to_date)
            calls_per_day_list, calls_per_day, date_list = self.calls_per_day(form.cleaned_data, from_date, to_date)
            per_day_chart = self.plot_line_chart(calls_per_day, date_list, "day")
            unique_app_names, number_of_apps_with_unique_app_name, number_of_apps_with_unique_developer_email = self.get_total_number_of_apps(form.cleaned_data, from_date, to_date)
            active_apps_list = self.get_active_apps(form.cleaned_data, from_date, to_date)

        context.update({
            'api_calls': api_calls,
            'calls_by_api_explorer': calls_by_api_explorer,
            'calls_per_month_list': calls_per_month_list,
            'per_day_chart': per_day_chart,
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
            'from_date': (datetime.datetime.strptime(from_date, API_DATEFORMAT)).strftime('%Y-%m-%d'),
            'to_date': (datetime.datetime.strptime(to_date, API_DATEFORMAT)).strftime('%Y-%m-%d'),
            'top_apis_bar_chart': top_apis_bar_chart,
            'median_time_to_first_api_call': median_time_to_first_api_call,
            'form': form,
            'excluded_apps':EXCLUDE_APPS,
            'excluded_functions':EXCLUDE_FUNCTIONS,
            'excluded_url_pattern':EXCLUDE_URL_PATTERN,
        })
        return context

class YearlySummaryView(MetricsSummaryView):
    template_name = 'metrics/yearly_summary.html'

    def get_context_data(self, **kwargs):
        form = self.get_form()
        to_date = datetime.datetime.strptime(form.data['to_date'], '%Y-%m-%d %H:%M:%S')
        to_date = to_date.strftime(API_DATEFORMAT)
        from_date = (datetime.datetime.strptime(to_date, API_DATEFORMAT) - timedelta(365)).strftime(API_DATEFORMAT)

        context = super(MetricsSummaryView, self).get_context_data(**kwargs)
        api_host_name = API_HOST
        top_apps_using_warehouse = self.get_top_apps_using_warehouse(from_date, to_date)
        user_email_cansearchwarehouse, number_of_users_with_cansearchwarehouse = self.get_users_cansearchwarehouse()
        median_time_to_first_api_call = self.median_time_to_first_api_call(from_date, to_date)

        if form.is_valid():
            api_calls, average_response_time, average_calls_per_day = self.get_aggregate_metrics(form.cleaned_data, from_date, to_date)
            calls_by_api_explorer, average_response_time_api_explorer, average_calls_per_day_api_explorer = self.get_aggregate_metrics_api_explorer(from_date, to_date)
            calls_per_month_list, calls_per_month, month_list = self.calls_per_month(form.cleaned_data, from_date, to_date)
            per_month_chart = self.plot_line_chart(calls_per_month, month_list[1:], "month")
            unique_app_names, number_of_apps_with_unique_app_name, number_of_apps_with_unique_developer_email = self.get_total_number_of_apps(form.cleaned_data, from_date, to_date)
            active_apps_names = self.get_active_apps(form.cleaned_data, from_date, to_date)
            top_apis = self.get_top_apis(form.cleaned_data, from_date, to_date)
            top_apis_bar_chart = self.plot_bar_chart(top_apis)
            top_warehouse_calls = self.get_top_warehouse_calls(form.cleaned_data, from_date, to_date)

        context.update({
            'api_calls': api_calls,
            'calls_by_api_explorer': calls_by_api_explorer,
            'calls_per_month_list': calls_per_month_list,
            'per_month_chart': per_month_chart,
            'number_of_apps_with_unique_app_name': number_of_apps_with_unique_app_name,
            'number_of_apps_with_unique_developer_email': number_of_apps_with_unique_developer_email,
            'active_apps_names': active_apps_names,
            'average_calls_per_day': average_calls_per_day,
            'average_response_time': average_response_time,
            'top_apis': top_apis,
            'top_warehouse_calls': top_warehouse_calls,
            'top_apps_using_warehouse': top_apps_using_warehouse,
            'user_email_cansearchwarehouse': user_email_cansearchwarehouse,
            'number_of_users_with_cansearchwarehouse': number_of_users_with_cansearchwarehouse,
            'api_host_name': api_host_name,
            'from_date': (datetime.datetime.strptime(from_date, API_DATEFORMAT)).strftime('%Y-%m-%d'),
            'to_date': (datetime.datetime.strptime(to_date, API_DATEFORMAT)).strftime('%Y-%m-%d'),
            'top_apis_bar_chart': top_apis_bar_chart,
            'median_time_to_first_api_call': median_time_to_first_api_call,
            'form': form,
            'excluded_apps':EXCLUDE_APPS,
            'excluded_functions':EXCLUDE_FUNCTIONS,
            'excluded_url_pattern':EXCLUDE_URL_PATTERN,
        })
        return context

class QuarterlySummaryView(MetricsSummaryView):
    template_name = 'metrics/quarterly_summary.html'

    def get_context_data(self, **kwargs):
        form = self.get_form()
        to_date = datetime.datetime.strptime(form.data['to_date'], '%Y-%m-%d %H:%M:%S')
        to_date = to_date.strftime(API_DATEFORMAT)
        from_date = (datetime.datetime.strptime(to_date, API_DATEFORMAT) - timedelta(90)).strftime(API_DATEFORMAT)

        context = super(MetricsSummaryView, self).get_context_data(**kwargs)
        api_host_name = API_HOST
        top_apps_using_warehouse = self.get_top_apps_using_warehouse(from_date, to_date)
        user_email_cansearchwarehouse, number_of_users_with_cansearchwarehouse = self.get_users_cansearchwarehouse()
        median_time_to_first_api_call = self.median_time_to_first_api_call(from_date, to_date)

        if form.is_valid():
            api_calls, average_response_time, average_calls_per_day = self.get_aggregate_metrics(form.cleaned_data, from_date, to_date)
            calls_by_api_explorer, average_response_time_api_explorer, average_calls_per_day_api_explorer = self.get_aggregate_metrics_api_explorer(from_date, to_date)
            calls_per_month_list, calls_per_month, month_list = self.calls_per_month(form.cleaned_data, from_date, to_date)
            calls_per_day_list, calls_per_day, date_list = self.calls_per_day(form.cleaned_data, from_date, to_date)
            per_month_chart = self.plot_line_chart(calls_per_month, month_list[1:], 'month')
            per_day_chart = self.plot_line_chart(calls_per_day, date_list, 'day')
            unique_app_names, number_of_apps_with_unique_app_name, number_of_apps_with_unique_developer_email = self.get_total_number_of_apps(form.cleaned_data, from_date, to_date)
            active_apps_names = self.get_active_apps(form.cleaned_data, from_date, to_date)
            top_apis = self.get_top_apis(form.cleaned_data, from_date, to_date)
            top_apis_bar_chart = self.plot_bar_chart(top_apis)
            top_warehouse_calls = self.get_top_warehouse_calls(form.cleaned_data, from_date, to_date)

        context.update({
            'api_calls': api_calls,
            'calls_by_api_explorer': calls_by_api_explorer,
            'calls_per_month_list': calls_per_month_list,
            'per_month_chart': per_month_chart,
            'per_day_chart': per_day_chart,
            'number_of_apps_with_unique_app_name': number_of_apps_with_unique_app_name,
            'number_of_apps_with_unique_developer_email': number_of_apps_with_unique_developer_email,
            'active_apps_names': active_apps_names,
            'average_calls_per_day': average_calls_per_day,
            'average_response_time': average_response_time,
            'top_apis': top_apis,
            'top_warehouse_calls': top_warehouse_calls,
            'top_apps_using_warehouse': top_apps_using_warehouse,
            'user_email_cansearchwarehouse': user_email_cansearchwarehouse,
            'number_of_users_with_cansearchwarehouse': number_of_users_with_cansearchwarehouse,
            'api_host_name': api_host_name,
            #'from_date': from_date.strftime('%Y-%m-%d'),
            'from_date': (datetime.datetime.strptime(from_date, API_DATEFORMAT)).strftime('%Y-%m-%d'),
            'to_date': (datetime.datetime.strptime(to_date, API_DATEFORMAT)).strftime('%Y-%m-%d'),
            'top_apis_bar_chart': top_apis_bar_chart,
            'median_time_to_first_api_call': median_time_to_first_api_call,
            'form': form,
            'excluded_apps':EXCLUDE_APPS,
            'excluded_functions':EXCLUDE_FUNCTIONS,
            'excluded_url_pattern':EXCLUDE_URL_PATTERN,
        })
        return context

class WeeklySummaryView(MetricsSummaryView):
    template_name = 'metrics/weekly_summary.html'

    def get_context_data(self, **kwargs):
        form = self.get_form()
        to_date = datetime.datetime.strptime(form.data['to_date'], '%Y-%m-%d %H:%M:%S')
        to_date = to_date.strftime(API_DATEFORMAT)
        from_date = (datetime.datetime.strptime(to_date, API_DATEFORMAT) - timedelta(7)).strftime(API_DATEFORMAT)

        context = super(MetricsSummaryView, self).get_context_data(**kwargs)
        api_host_name = API_HOST
        top_apps_using_warehouse = self.get_top_apps_using_warehouse(from_date, to_date)
        user_email_cansearchwarehouse, number_of_users_with_cansearchwarehouse = self.get_users_cansearchwarehouse()
        # calls_per_half_day = self.calls_per_half_day()
        median_time_to_first_api_call = self.median_time_to_first_api_call(from_date, to_date)

        if form.is_valid():
            api_calls, average_response_time, average_calls_per_day = self.get_aggregate_metrics(form.cleaned_data, from_date, to_date)
            calls_by_api_explorer, average_response_time_api_explorer, average_calls_per_day_api_explorer = self.get_aggregate_metrics_api_explorer(from_date, to_date)
            calls_per_day_list, calls_per_day, date_list = self.calls_per_day(form.cleaned_data, from_date, to_date)
            per_day_chart = self.plot_line_chart(calls_per_day, date_list[1:], 'day')
            unique_app_names, number_of_apps_with_unique_app_name, number_of_apps_with_unique_developer_email = self.get_total_number_of_apps(form.cleaned_data, from_date, to_date)
            active_apps_names = self.get_active_apps(form.cleaned_data, from_date, to_date)
            top_apis = self.get_top_apis(form.cleaned_data, from_date, to_date)
            top_apis_bar_chart = self.plot_bar_chart(top_apis)
            top_warehouse_calls = self.get_top_warehouse_calls(form.cleaned_data, from_date, to_date)

        context.update({
            'api_calls': api_calls,
            'calls_by_api_explorer': calls_by_api_explorer,
            'per_day_chart': per_day_chart,
            'number_of_apps_with_unique_app_name': number_of_apps_with_unique_app_name,
            'number_of_apps_with_unique_developer_email': number_of_apps_with_unique_developer_email,
            'active_apps_names': active_apps_names,
            'average_calls_per_day': average_calls_per_day,
            'average_response_time': average_response_time,
            'top_apis': top_apis,
            'top_warehouse_calls': top_warehouse_calls,
            'top_apps_using_warehouse': top_apps_using_warehouse,
            'user_email_cansearchwarehouse': user_email_cansearchwarehouse,
            'number_of_users_with_cansearchwarehouse': number_of_users_with_cansearchwarehouse,
            'api_host_name': api_host_name,
            'from_date': (datetime.datetime.strptime(from_date, API_DATEFORMAT)).strftime('%Y-%m-%d'),
            'to_date': (datetime.datetime.strptime(to_date, API_DATEFORMAT)).strftime('%Y-%m-%d'),
            'top_apis_bar_chart': top_apis_bar_chart,
            # ##'calls_per_half_day': calls_per_half_day,
            'median_time_to_first_api_call': median_time_to_first_api_call,
            'form': form,
            'excluded_apps':EXCLUDE_APPS,
            'excluded_functions':EXCLUDE_FUNCTIONS,
            'excluded_url_pattern':EXCLUDE_URL_PATTERN,
        })
        return context


class DailySummaryView(MetricsSummaryView):
    template_name = 'metrics/daily_summary.html'

    def get_context_data(self, **kwargs):
        form = self.get_form()
        to_date = datetime.datetime.strptime(form.data['to_date'], '%Y-%m-%d %H:%M:%S')
        to_date = to_date.strftime(API_DATEFORMAT)
        from_date = (datetime.datetime.strptime(to_date, API_DATEFORMAT) - timedelta(1)).strftime(API_DATEFORMAT)

        context = super(DailySummaryView, self).get_context_data(**kwargs)
        api_host_name = API_HOST
        top_apps_using_warehouse = self.get_top_apps_using_warehouse(from_date, to_date)
        user_email_cansearchwarehouse, number_of_users_with_cansearchwarehouse = self.get_users_cansearchwarehouse()
        median_time_to_first_api_call = self.median_time_to_first_api_call(from_date, to_date)

        if form.is_valid():
            api_calls, average_response_time, average_calls_per_day = self.get_aggregate_metrics(form.cleaned_data, from_date, to_date)
            calls_by_api_explorer, average_response_time_api_explorer, average_calls_per_day_api_explorer = self.get_aggregate_metrics_api_explorer(from_date, to_date)
            calls_per_hour_list, calls_per_hour, hour_list = self.calls_per_hour(form.cleaned_data, from_date, to_date)
            per_hour_chart = self.plot_line_chart(calls_per_hour, hour_list[1:], 'hour')
 #           calls_per_hour_list, calls_per_hour = self.calls_per_hour(form.cleaned_data, from_date)
 #           per_hour_chart = self.get_per_hour_chart(form.cleaned_data, from_date)
            unique_app_names, number_of_apps_with_unique_app_name, number_of_apps_with_unique_developer_email = self.get_total_number_of_apps(form.cleaned_data, from_date, to_date)
            active_apps_names = self.get_active_apps(form.cleaned_data, from_date, to_date)
            top_apis = self.get_top_apis(form.cleaned_data, from_date, to_date)
            top_apis_bar_chart = self.plot_bar_chart(top_apis)
            top_warehouse_calls = self.get_top_warehouse_calls(form.cleaned_data, from_date, to_date)

        context.update({
            'api_calls': api_calls,
            'calls_by_api_explorer': calls_by_api_explorer,
            'calls_per_hour_list': calls_per_hour_list,
            'per_hour_chart': per_hour_chart,
            'number_of_apps_with_unique_app_name': number_of_apps_with_unique_app_name,
            'number_of_apps_with_unique_developer_email': number_of_apps_with_unique_developer_email,
            'active_apps_names': active_apps_names,
            'average_calls_per_day': average_calls_per_day,
            'average_response_time': average_response_time,
            'top_apis': top_apis,
            'top_warehouse_calls': top_warehouse_calls,
            'top_apps_using_warehouse': top_apps_using_warehouse,
            'user_email_cansearchwarehouse': user_email_cansearchwarehouse,
            'number_of_users_with_cansearchwarehouse': number_of_users_with_cansearchwarehouse,
            'api_host_name': api_host_name,
            'from_date': (datetime.datetime.strptime(from_date, API_DATEFORMAT)).strftime('%Y-%m-%d'),
            'to_date': (datetime.datetime.strptime(to_date, API_DATEFORMAT)).strftime('%Y-%m-%d'),
            'top_apis_bar_chart': top_apis_bar_chart,
            'median_time_to_first_api_call': median_time_to_first_api_call,
            'form': form,
            'excluded_apps':EXCLUDE_APPS,
            'excluded_functions':EXCLUDE_FUNCTIONS,
            'excluded_url_pattern':EXCLUDE_URL_PATTERN,
        })
        return context

class HourlySummaryView(MetricsSummaryView):
    template_name = 'metrics/hourly_summary.html'

class CustomSummaryView(MetricsSummaryView):
    form_class = CustomSummaryForm
    template_name = 'metrics/custom_summary.html'

    def get_context_data(self, **kwargs):
        form = self.get_form()

        to_date = datetime.datetime.strptime(form.data['to_date'], '%Y-%m-%d %H:%M:%S')
        to_date = to_date.strftime(API_DATEFORMAT)

        from_date = datetime.datetime.strptime(form.data['from_date_custom'], '%Y-%m-%d %H:%M:%S')
        from_date = from_date.strftime(API_DATEFORMAT)
        context = super(MetricsSummaryView, self).get_context_data(**kwargs)
        api_host_name = API_HOST
        top_apps_using_warehouse = self.get_top_apps_using_warehouse(from_date, to_date)
        user_email_cansearchwarehouse, number_of_users_with_cansearchwarehouse = self.get_users_cansearchwarehouse()
        # calls_per_day = self.calls_per_day(from_date)
        # calls_per_half_day = self.calls_per_half_day()
        median_time_to_first_api_call = self.median_time_to_first_api_call(from_date, to_date)

        if form.is_valid():
            api_calls, average_response_time, average_calls_per_day = self.get_aggregate_metrics(form.cleaned_data, from_date, to_date)
            calls_by_api_explorer, average_response_time_api_explorer, average_calls_per_day_api_explorer = self.get_aggregate_metrics_api_explorer(from_date, to_date)
            calls_per_day_list, calls_per_day, date_list = self.calls_per_day(form.cleaned_data, from_date, to_date)
            per_day_chart = self.plot_line_chart(calls_per_day, date_list[1:], 'day')
            unique_app_names, number_of_apps_with_unique_app_name, number_of_apps_with_unique_developer_email = self.get_total_number_of_apps(form.cleaned_data, from_date, to_date)
            active_apps_names = self.get_active_apps(form.cleaned_data, from_date, to_date)
            top_apis = self.get_top_apis(form.cleaned_data, from_date, to_date)
            top_apis_bar_chart = self.plot_bar_chart(top_apis)
            top_warehouse_calls = self.get_top_warehouse_calls(form.cleaned_data, from_date, to_date)

        context.update({
            'api_calls': api_calls,
            'calls_by_api_explorer': calls_by_api_explorer,
            'per_day_chart': per_day_chart,
            'number_of_apps_with_unique_app_name': number_of_apps_with_unique_app_name,
            'number_of_apps_with_unique_developer_email': number_of_apps_with_unique_developer_email,
            'active_apps_names': active_apps_names,
            'average_calls_per_day': average_calls_per_day,
            'average_response_time': average_response_time,
            'top_apis': top_apis,
            'top_warehouse_calls': top_warehouse_calls,
            'top_apps_using_warehouse': top_apps_using_warehouse,
            'user_email_cansearchwarehouse': user_email_cansearchwarehouse,
            'number_of_users_with_cansearchwarehouse': number_of_users_with_cansearchwarehouse,
            'api_host_name': api_host_name,
            'from_date': (datetime.datetime.strptime(from_date, API_DATEFORMAT)).strftime('%Y-%m-%d'),
            'to_date': (datetime.datetime.strptime(to_date, API_DATEFORMAT)).strftime('%Y-%m-%d'),
            'top_apis_bar_chart': top_apis_bar_chart,
            'median_time_to_first_api_call': median_time_to_first_api_call,
            # ##'calls_per_day': calls_per_day,
            # ##'calls_per_half_day': calls_per_half_day,
            'form': form,
            'excluded_apps':EXCLUDE_APPS,
            'excluded_functions':EXCLUDE_FUNCTIONS,
            'excluded_url_pattern':EXCLUDE_URL_PATTERN,
        })
        return context