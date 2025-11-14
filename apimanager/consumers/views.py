# -*- coding: utf-8 -*-
"""
Views of consumers app
"""

from datetime import datetime
import datetime as dt_module
import json

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import TemplateView, RedirectView, FormView
from django.http import JsonResponse, HttpResponseRedirect

from obp.api import API, APIError
from base.filters import BaseFilter, FilterTime

from .forms import ApiConsumersForm


class FilterAppType(BaseFilter):
    """Filter consumers by application type"""

    filter_type = "app_type"

    def _apply(self, data, filter_value):
        filtered = [x for x in data if x["app_type"] == filter_value]
        return filtered


class FilterEnabled(BaseFilter):
    """Filter consumers by enabled state"""

    filter_type = "enabled"

    def _apply(self, data, filter_value):
        enabled = filter_value in ["true"]
        filtered = [x for x in data if x["enabled"] == enabled]
        return filtered


class IndexView(LoginRequiredMixin, TemplateView):
    """Index view for consumers"""

    template_name = "consumers/index.html"

    def scrub(self, consumers):
        """Scrubs data in the given consumers to adher to certain formats"""
        for consumer in consumers:
            consumer["created"] = datetime.strptime(
                consumer["created"], settings.API_DATE_FORMAT_WITH_SECONDS
            )
        return consumers

    def compile_statistics(self, consumers):
        """Compiles a set of statistical values for the given consumers"""
        unique_developer_email = {}
        unique_name = {}
        for consumer in consumers:
            unique_developer_email[consumer["developer_email"]] = True
            unique_name[consumer["app_name"]] = True
        unique_developer_email = unique_developer_email.keys()
        unique_name = unique_name.keys()
        statistics = {
            "consumers_num": len(consumers),
            "unique_developer_email_num": len(unique_developer_email),
            "unique_name_num": len(unique_name),
        }
        return statistics

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        consumers = []
        sorted_consumers = []
        api = API(self.request.session.get("obp"))
        try:
            limit = self.request.GET.get("limit", 50)
            offset = self.request.GET.get("offset", 0)
            urlpath = "/management/consumers?limit={}&offset={}".format(limit, offset)
            consumers = api.get(urlpath)
            if "code" in consumers and consumers["code"] >= 400:
                messages.error(self.request, consumers["message"])
            else:
                consumers = FilterEnabled(context, self.request.GET).apply(
                    consumers["consumers"]
                )
                consumers = FilterAppType(context, self.request.GET).apply(consumers)
                consumers = FilterTime(context, self.request.GET, "created").apply(
                    consumers
                )
                consumers = self.scrub(consumers)
                sorted_consumers = sorted(
                    consumers, key=lambda consumer: consumer["created"], reverse=True
                )

                context.update(
                    {
                        "consumers": sorted_consumers,
                        "limit": limit,
                        "offset": offset,
                        "statistics": self.compile_statistics(consumers),
                    }
                )
        except APIError as err:
            messages.error(self.request, err)

        return context


class DetailView(LoginRequiredMixin, FormView):
    """Detail view for a consumer"""

    form_class = ApiConsumersForm
    template_name = "consumers/detail.html"

    def dispatch(self, request, *args, **kwargs):
        self.api = API(request.session.get("obp"))
        return super(DetailView, self).dispatch(request, *args, **kwargs)

    def get_form(self, *args, **kwargs):
        form = super(DetailView, self).get_form(*args, **kwargs)
        form.fields["consumer_id"].initial = self.kwargs["consumer_id"]

        # Get call limits data to populate form
        api = API(self.request.session.get("obp"))
        try:
            call_limits_urlpath = (
                "/management/consumers/{}/consumer/rate-limits".format(
                    self.kwargs["consumer_id"]
                )
            )
            call_limits = api.get(call_limits_urlpath)

            if not ("code" in call_limits and call_limits["code"] >= 400):
                # Populate form with existing rate limiting data
                if "from_date" in call_limits and call_limits["from_date"]:
                    try:
                        from_date_str = call_limits["from_date"].replace("Z", "")
                        # Parse and ensure no timezone info for form field
                        dt = datetime.fromisoformat(from_date_str)
                        if dt.tzinfo:
                            dt = dt.replace(tzinfo=None)
                        form.fields["from_date"].initial = dt
                    except:
                        pass
                if "to_date" in call_limits and call_limits["to_date"]:
                    try:
                        to_date_str = call_limits["to_date"].replace("Z", "")
                        # Parse and ensure no timezone info for form field
                        dt = datetime.fromisoformat(to_date_str)
                        if dt.tzinfo:
                            dt = dt.replace(tzinfo=None)
                        form.fields["to_date"].initial = dt
                    except:
                        pass
                form.fields["per_second_call_limit"].initial = call_limits.get(
                    "per_second_call_limit", "-1"
                )
                form.fields["per_minute_call_limit"].initial = call_limits.get(
                    "per_minute_call_limit", "-1"
                )
                form.fields["per_hour_call_limit"].initial = call_limits.get(
                    "per_hour_call_limit", "-1"
                )
                form.fields["per_day_call_limit"].initial = call_limits.get(
                    "per_day_call_limit", "-1"
                )
                form.fields["per_week_call_limit"].initial = call_limits.get(
                    "per_week_call_limit", "-1"
                )
                form.fields["per_month_call_limit"].initial = call_limits.get(
                    "per_month_call_limit", "-1"
                )
        except:
            pass

        return form

    def post(self, request, *args, **kwargs):
        """Handle POST requests for rate limit CRUD operations"""
        action = request.POST.get("action")

        # Check if this is an AJAX request
        if request.headers.get("X-Requested-With") == "XMLHttpRequest" or action in [
            "create",
            "update",
            "delete",
        ]:
            if action == "create":
                return self.create_rate_limit(request)
            elif action == "update":
                return self.update_rate_limit(request)
            elif action == "delete":
                return self.delete_rate_limit(request)

        # Fallback to original form handling for compatibility
        form = self.get_form()
        if form.is_valid():
            return self.form_valid_legacy(request, form)
        else:
            return self.form_invalid(form)

    def create_rate_limit(self, request):
        """Create a new rate limit using v6.0.0 POST API"""
        try:
            consumer_id = self.kwargs["consumer_id"]

            # Helper function to format datetime to UTC
            def format_datetime_utc(dt_str):
                if not dt_str:
                    return "2024-01-01T00:00:00Z"
                try:
                    dt = datetime.fromisoformat(dt_str)
                    return dt.strftime("%Y-%m-%dT%H:%M:%SZ")
                except:
                    return "2024-01-01T00:00:00Z"

            payload = {
                "from_date": format_datetime_utc(request.POST.get("from_date")),
                "to_date": format_datetime_utc(request.POST.get("to_date")),
                "per_second_call_limit": str(
                    request.POST.get("per_second_call_limit", "-1")
                ),
                "per_minute_call_limit": str(
                    request.POST.get("per_minute_call_limit", "-1")
                ),
                "per_hour_call_limit": str(
                    request.POST.get("per_hour_call_limit", "-1")
                ),
                "per_day_call_limit": str(request.POST.get("per_day_call_limit", "-1")),
                "per_week_call_limit": str(
                    request.POST.get("per_week_call_limit", "-1")
                ),
                "per_month_call_limit": str(
                    request.POST.get("per_month_call_limit", "-1")
                ),
            }

            # Use v6.0.0 API for creating rate limits
            urlpath = "/management/consumers/{}/consumer/rate-limits".format(
                consumer_id
            )
            response = self.api.post(
                urlpath, payload, version=settings.API_VERSION["v600"]
            )

            if "code" in response and response["code"] >= 400:
                messages.error(request, response["message"])
            else:
                messages.success(request, "Rate limit created successfully.")

        except APIError as err:
            messages.error(request, str(err))
        except Exception as err:
            messages.error(request, "Error creating rate limit: {}".format(err))

        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return JsonResponse({"success": True, "redirect": request.path})
        else:
            return HttpResponseRedirect(request.path)

    def update_rate_limit(self, request):
        """Update existing rate limit using v6.0.0 PUT API"""
        try:
            consumer_id = self.kwargs["consumer_id"]
            rate_limiting_id = request.POST.get("rate_limit_id")

            if not rate_limiting_id:
                messages.error(request, "Rate limiting ID is required for update.")
                return JsonResponse(
                    {"success": False, "error": "Missing rate limiting ID"}
                )

            # Helper function to format datetime to UTC
            def format_datetime_utc(dt_str):
                if not dt_str:
                    return "2024-01-01T00:00:00Z"
                try:
                    dt = datetime.fromisoformat(dt_str)
                    return dt.strftime("%Y-%m-%dT%H:%M:%SZ")
                except:
                    return "2024-01-01T00:00:00Z"

            payload = {
                "from_date": format_datetime_utc(request.POST.get("from_date")),
                "to_date": format_datetime_utc(request.POST.get("to_date")),
                "per_second_call_limit": str(
                    request.POST.get("per_second_call_limit", "-1")
                ),
                "per_minute_call_limit": str(
                    request.POST.get("per_minute_call_limit", "-1")
                ),
                "per_hour_call_limit": str(
                    request.POST.get("per_hour_call_limit", "-1")
                ),
                "per_day_call_limit": str(request.POST.get("per_day_call_limit", "-1")),
                "per_week_call_limit": str(
                    request.POST.get("per_week_call_limit", "-1")
                ),
                "per_month_call_limit": str(
                    request.POST.get("per_month_call_limit", "-1")
                ),
            }

            # Use v6.0.0 API for updating rate limits with rate_limiting_id
            urlpath = "/management/consumers/{}/consumer/rate-limits/{}".format(
                consumer_id, rate_limiting_id
            )
            response = self.api.put(
                urlpath, payload, version=settings.API_VERSION["v600"]
            )

            if "code" in response and response["code"] >= 400:
                messages.error(request, response["message"])
            else:
                messages.success(request, "Rate limit updated successfully.")

        except APIError as err:
            messages.error(request, str(err))
        except Exception as err:
            messages.error(request, "Error updating rate limit: {}".format(err))

        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return JsonResponse({"success": True, "redirect": request.path})
        else:
            return HttpResponseRedirect(request.path)

    def delete_rate_limit(self, request):
        """Delete a rate limit using v6.0.0 DELETE API"""
        try:
            consumer_id = self.kwargs["consumer_id"]
            rate_limiting_id = request.POST.get("rate_limiting_id")

            if not rate_limiting_id:
                messages.error(request, "Rate limiting ID is required for deletion.")
                return JsonResponse(
                    {"success": False, "error": "Missing rate limiting ID"}
                )

            # Use v6.0.0 API for deleting rate limits
            urlpath = "/management/consumers/{}/consumer/rate-limits/{}".format(
                consumer_id, rate_limiting_id
            )
            response = self.api.delete(urlpath, version=settings.API_VERSION["v600"])

            if "code" in response and response["code"] >= 400:
                messages.error(request, response["message"])
            else:
                messages.success(request, "Rate limit deleted successfully.")

        except APIError as err:
            messages.error(request, str(err))
        except Exception as err:
            messages.error(request, "Error deleting rate limit: {}".format(err))

        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return JsonResponse({"success": True, "redirect": request.path})
        else:
            return HttpResponseRedirect(request.path)

    def form_valid_legacy(self, request, form):
        """Legacy form handling for backwards compatibility"""
        try:
            data = form.cleaned_data

            urlpath = "/management/consumers/{}/consumer/rate-limits".format(
                data["consumer_id"]
            )

            # Helper function to format datetime to UTC
            def format_datetime_utc(dt):
                if not dt:
                    return "2024-01-01T00:00:00Z"
                # Convert to UTC and format as required by API
                if dt.tzinfo:
                    dt = dt.astimezone(dt_module.timezone.utc).replace(tzinfo=None)
                return dt.strftime("%Y-%m-%dT%H:%M:%SZ")

            payload = {
                "from_date": format_datetime_utc(data["from_date"]),
                "to_date": format_datetime_utc(data["to_date"]),
                "per_second_call_limit": str(data["per_second_call_limit"])
                if data["per_second_call_limit"] is not None
                else "-1",
                "per_minute_call_limit": str(data["per_minute_call_limit"])
                if data["per_minute_call_limit"] is not None
                else "-1",
                "per_hour_call_limit": str(data["per_hour_call_limit"])
                if data["per_hour_call_limit"] is not None
                else "-1",
                "per_day_call_limit": str(data["per_day_call_limit"])
                if data["per_day_call_limit"] is not None
                else "-1",
                "per_week_call_limit": str(data["per_week_call_limit"])
                if data["per_week_call_limit"] is not None
                else "-1",
                "per_month_call_limit": str(data["per_month_call_limit"])
                if data["per_month_call_limit"] is not None
                else "-1",
            }

            response = self.api.put(
                urlpath, payload, version=settings.API_VERSION["v510"]
            )
            if "code" in response and response["code"] >= 400:
                messages.error(request, response["message"])
                return super(DetailView, self).form_invalid(form)

        except APIError as err:
            messages.error(request, err)
            return super(DetailView, self).form_invalid(form)
        except Exception as err:
            messages.error(request, "{}".format(err))
            return super(DetailView, self).form_invalid(form)

        msg = "Rate limits for consumer {} have been updated successfully.".format(
            data["consumer_id"]
        )
        messages.success(request, msg)
        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return JsonResponse({"success": True, "redirect": request.path})
        else:
            return HttpResponseRedirect(request.path)

    def get(self, request, *args, **kwargs):
        # Check if this is an AJAX request for usage data
        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return self.get_usage_data_ajax()
        return super(DetailView, self).get(request, *args, **kwargs)

    def get_usage_data_ajax(self):
        """Return usage data as JSON for AJAX refresh"""
        api = API(self.request.session.get("obp"))
        try:
            call_limits_urlpath = (
                "/management/consumers/{}/consumer/rate-limits".format(
                    self.kwargs["consumer_id"]
                )
            )
            call_limits = api.get(call_limits_urlpath)

            if "code" in call_limits and call_limits["code"] >= 400:
                return JsonResponse({"error": call_limits["message"]}, status=400)

            return JsonResponse(call_limits)
        except APIError as err:
            return JsonResponse({"error": str(err)}, status=500)
        except Exception as err:
            return JsonResponse({"error": str(err)}, status=500)

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        api = API(self.request.session.get("obp"))
        consumer = {}
        call_limits = {}
        # Initialize current_usage with default values
        current_usage = {
            "per_second": {"calls_made": -1, "reset_in_seconds": -1},
            "per_minute": {"calls_made": -1, "reset_in_seconds": -1},
            "per_hour": {"calls_made": -1, "reset_in_seconds": -1},
            "per_day": {"calls_made": -1, "reset_in_seconds": -1},
            "per_week": {"calls_made": -1, "reset_in_seconds": -1},
            "per_month": {"calls_made": -1, "reset_in_seconds": -1},
        }

        try:
            urlpath = "/management/consumers/{}".format(self.kwargs["consumer_id"])
            consumer = api.get(urlpath)
            if "code" in consumer and consumer["code"] >= 400:
                messages.error(self.request, consumer["message"])
                consumer = {}
            else:
                consumer["created"] = datetime.strptime(
                    consumer["created"], settings.API_DATE_FORMAT_WITH_SECONDS
                )

            # Get call limits using the correct API endpoint
            call_limits_urlpath = (
                "/management/consumers/{}/consumer/rate-limits".format(
                    self.kwargs["consumer_id"]
                )
            )
            call_limits = api.get(
                call_limits_urlpath, version=settings.API_VERSION["v510"]
            )

            # Get current usage data using v6.0.0 API
            current_usage_urlpath = (
                "/management/consumers/{}/consumer/current-usage".format(
                    self.kwargs["consumer_id"]
                )
            )
            current_usage = api.get(
                current_usage_urlpath, version=settings.API_VERSION["v600"]
            )
            if "code" in current_usage and current_usage["code"] >= 400:
                # If current usage fails, keep the default values already set
                pass

            if "code" in call_limits and call_limits["code"] >= 400:
                messages.error(self.request, "{}".format(call_limits["message"]))
                call_limits = {"limits": []}
            else:
                # Handle different API response structures
                import uuid

                # Handle case where API returns data directly instead of in 'limits' array
                if (
                    "limits" not in call_limits
                    and "per_second_call_limit" in call_limits
                ):
                    # API returned single limit object, wrap it in limits array
                    if "rate_limiting_id" not in call_limits:
                        call_limits["rate_limiting_id"] = str(uuid.uuid4())
                    call_limits = {"limits": [call_limits]}
                elif "limits" not in call_limits:
                    # No limits data found
                    call_limits = {"limits": []}
                else:
                    # Ensure each limit has a rate_limiting_id
                    for limit in call_limits.get("limits", []):
                        if (
                            "rate_limiting_id" not in limit
                            or not limit["rate_limiting_id"]
                        ):
                            limit["rate_limiting_id"] = str(uuid.uuid4())

                # For backwards compatibility, merge first limit into consumer if limits exist
                if call_limits.get("limits") and len(call_limits["limits"]) > 0:
                    first_limit = call_limits["limits"][0]
                    consumer.update(
                        {
                            "from_date": first_limit.get("from_date", ""),
                            "to_date": first_limit.get("to_date", ""),
                            "per_second_call_limit": first_limit.get(
                                "per_second_call_limit", "-1"
                            ),
                            "per_minute_call_limit": first_limit.get(
                                "per_minute_call_limit", "-1"
                            ),
                            "per_hour_call_limit": first_limit.get(
                                "per_hour_call_limit", "-1"
                            ),
                            "per_day_call_limit": first_limit.get(
                                "per_day_call_limit", "-1"
                            ),
                            "per_week_call_limit": first_limit.get(
                                "per_week_call_limit", "-1"
                            ),
                            "per_month_call_limit": first_limit.get(
                                "per_month_call_limit", "-1"
                            ),
                            "current_state": call_limits.get("current_state", {}),
                            "created_at": first_limit.get("created_at", ""),
                            "updated_at": first_limit.get("updated_at", ""),
                        }
                    )

        except APIError as err:
            messages.error(self.request, err)
        except Exception as err:
            messages.error(self.request, "{}".format(err))
        finally:
            # Ensure current_usage always has the expected structure
            if not current_usage or "per_second" not in current_usage:
                current_usage = {
                    "per_second": {"calls_made": -1, "reset_in_seconds": -1},
                    "per_minute": {"calls_made": -1, "reset_in_seconds": -1},
                    "per_hour": {"calls_made": -1, "reset_in_seconds": -1},
                    "per_day": {"calls_made": -1, "reset_in_seconds": -1},
                    "per_week": {"calls_made": -1, "reset_in_seconds": -1},
                    "per_month": {"calls_made": -1, "reset_in_seconds": -1},
                }
            context.update({"consumer": consumer, "call_limits": call_limits, "current_usage": current_usage})
        return context


class UsageDataAjaxView(LoginRequiredMixin, TemplateView):
    """AJAX view to return current usage data for real-time updates"""

    def get(self, request, *args, **kwargs):
        api = API(self.request.session.get("obp"))
        try:
            current_usage_urlpath = (
                "/management/consumers/{}/consumer/current-usage".format(
                    self.kwargs["consumer_id"]
                )
            )
            current_usage = api.get(
                current_usage_urlpath, version=settings.API_VERSION["v600"]
            )

            if "code" in current_usage and current_usage["code"] >= 400:
                return JsonResponse({"error": current_usage["message"]}, status=400)

            return JsonResponse(current_usage)
        except APIError as err:
            return JsonResponse({"error": str(err)}, status=500)
        except Exception as err:
            return JsonResponse({"error": str(err)}, status=500)


class EnableDisableView(LoginRequiredMixin, RedirectView):
    """View to enable or disable a consumer"""

    enabled = False
    success = None

    def get_redirect_url(self, *args, **kwargs):
        api = API(self.request.session.get("obp"))
        try:
            urlpath = "/management/consumers/{}".format(kwargs["consumer_id"])
            payload = {"enabled": self.enabled}
            response = api.put(urlpath, payload)
            if "code" in response and response["code"] >= 400:
                messages.error(self.request, response["message"])
            else:
                messages.success(self.request, self.success)
        except APIError as err:
            messages.error(self.request, err)

        urlpath = self.request.POST.get("next", reverse("consumers-index"))
        query = self.request.GET.urlencode()
        redirect_url = "{}?{}".format(urlpath, query)
        return redirect_url


class EnableView(EnableDisableView):
    """View to enable a consumer"""

    enabled = True
    success = "Consumer has been enabled."


class DisableView(EnableDisableView):
    """View to disable a consumer"""

    enabled = False
    success = "Consumer has been disabled."
