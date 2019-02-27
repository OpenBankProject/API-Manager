# -*- coding: utf-8 -*-
"""
Views of consumers app
"""

from datetime import datetime

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import TemplateView, RedirectView, FormView

from obp.api import API, APIError
from base.filters import BaseFilter, FilterTime

from .forms import ApiConsumersForm

# import logging
# logger = logging.getLogger(__name__)


class FilterAppType(BaseFilter):
    """Filter consumers by application type"""
    filter_type = 'app_type'

    def _apply(self, data, filter_value):
        filtered = [x for x in data if x['app_type'] == filter_value]
        return filtered


class FilterEnabled(BaseFilter):
    """Filter consumers by enabled state"""
    filter_type = 'enabled'

    def _apply(self, data, filter_value):
        enabled = filter_value in ['true']
        filtered = [x for x in data if x['enabled'] == enabled]
        return filtered


class IndexView(LoginRequiredMixin, TemplateView):
    """Index view for consumers"""
    template_name = "consumers/index.html"

    def scrub(self, consumers):
        """Scrubs data in the given consumers to adher to certain formats"""
        for consumer in consumers:
            consumer['created'] = datetime.strptime(
                consumer['created'], settings.API_DATETIMEFORMAT)
        return consumers

    def compile_statistics(self, consumers):
        """Compiles a set of statistical values for the given consumers"""
        unique_developer_email = {}
        unique_name = {}
        for consumer in consumers:
            unique_developer_email[consumer['developer_email']] = True
            unique_name[consumer['app_name']] = True
        unique_developer_email = unique_developer_email.keys()
        unique_name = unique_name.keys()
        statistics = {
            'consumers_num': len(consumers),
            'unique_developer_email_num': len(unique_developer_email),
            'unique_name_num': len(unique_name),
        }
        return statistics

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        consumers = []
        sorted_consumers=[]
        api = API(self.request.session.get('obp'))
        try:
            urlpath = '/management/consumers'
            consumers = api.get(urlpath)
            if 'code' in consumers and consumers['code']==403:
                messages.error(self.request, consumers['message'])
            else:
                consumers = FilterEnabled(context, self.request.GET)\
                    .apply(consumers['list'])
                consumers = FilterAppType(context, self.request.GET)\
                    .apply(consumers)
                consumers = FilterTime(context, self.request.GET, 'created')\
                    .apply(consumers)
                consumers = self.scrub(consumers)
                sorted_consumers = sorted(
                    consumers, key=lambda consumer: consumer['created'], reverse=True)

                context.update({
                    'consumers': sorted_consumers,
                    'statistics': self.compile_statistics(consumers),
                })
        except APIError as err:
            messages.error(self.request, err)

        return context


class DetailView(LoginRequiredMixin, FormView):
    """Detail view for a consumer"""
    form_class = ApiConsumersForm
    template_name = "consumers/detail.html"

    def dispatch(self, request, *args, **kwargs):
        self.api = API(request.session.get('obp'))
        return super(DetailView, self).dispatch(request, *args, **kwargs)

    def get_form(self, *args, **kwargs):
        form = super(DetailView, self).get_form(*args, **kwargs)
        form.fields['consumer_id'].initial = self.kwargs['consumer_id']
        return form

    def form_valid(self, form):

        """Put limits data to API"""
        try:
            data = ''
            form = ApiConsumersForm(self.request.POST)
            if form.is_valid():
                data = form.cleaned_data

            urlpath = '/management/consumers/{}/consumer/calls_limit'.format(data['consumer_id'])

            payload = {
                'per_minute_call_limit': data['per_minute_call_limit'],
                'per_hour_call_limit': data['per_hour_call_limit'],
                'per_day_call_limit': data['per_day_call_limit'],
                'per_week_call_limit': data['per_week_call_limit'],
                'per_month_call_limit': data['per_month_call_limit']
            }
            user = self.api.put(urlpath, payload=payload)
        except APIError as err:
            messages.error(self.request, err)
            return super(DetailView, self).form_invalid(form)
        except Exception as err:
            messages.error(self.request, "{}".format(err))
            return super(DetailView, self).form_invalid(form)

        msg = 'calls limit of consumer {} has been updated successfully.'.format(
            data['consumer_id'])
        messages.success(self.request, msg)
        self.success_url = self.request.path
        return super(DetailView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        api = API(self.request.session.get('obp'))
        try:
            urlpath = '/management/consumers/{}'.format(self.kwargs['consumer_id'])
            consumer = api.get(urlpath)
            consumer['created'] = datetime.strptime(
                consumer['created'], settings.API_DATETIMEFORMAT)

            call_limits_urlpath = '/management/consumers/{}/consumer/call-limits'.format(self.kwargs['consumer_id'])
            consumer_call_limtis = api.get(call_limits_urlpath)
            if 'code' in consumer_call_limtis and consumer_call_limtis['code'] > 400:
                messages.error(self.request, "{}".format(consumer_call_limtis['message']))
            else:
                consumer['per_minute_call_limit'] = consumer_call_limtis['per_minute_call_limit']
                consumer['per_hour_call_limit'] = consumer_call_limtis['per_hour_call_limit']
                consumer['per_day_call_limit'] = consumer_call_limtis['per_day_call_limit']
                consumer['per_week_call_limit'] = consumer_call_limtis['per_week_call_limit']
                consumer['per_month_call_limit'] = consumer_call_limtis['per_month_call_limit']

        except APIError as err:
            messages.error(self.request, err)
        except Exception as err:
            messages.error(self.request, "{}".format(err))
        finally:
            context.update({
                'consumer': consumer
            })
        return context


class EnableDisableView(LoginRequiredMixin, RedirectView):
    """View to enable or disable a consumer"""
    enabled = False
    success = None

    def get_redirect_url(self, *args, **kwargs):
        api = API(self.request.session.get('obp'))
        try:
            urlpath = '/management/consumers/{}'.format(kwargs['consumer_id'])
            payload = {'enabled': self.enabled}
            api.put(urlpath, payload)
            messages.success(self.request, self.success)
        except APIError as err:
            messages.error(self.request, err)
        except:
            messages.error(self.request, "Unknown")

        urlpath = self.request.POST.get('next', reverse('consumers-index'))
        query = self.request.GET.urlencode()
        redirect_url = '{}?{}'.format(urlpath, query)
        return redirect_url


class EnableView(EnableDisableView):
    """View to enable a consumer"""
    enabled = True
    success = "Consumer has been enabled."


class DisableView(EnableDisableView):
    """View to disable a consumer"""
    enabled = False
    success = "Consumer has been disabled."
