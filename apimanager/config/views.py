# -*- coding: utf-8 -*-
"""
Views of config app
"""

import json

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from obp.api import API, APIError


class IndexView(LoginRequiredMixin, TemplateView):
    """Index view for config"""
    template_name = "config/index.html"

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        api = API(self.request.session.get('obp'))
        try:
            urlpath = '/config'
            config = api.get(urlpath)
        except APIError as err:
            messages.error(self.request, err)
            config = {}
        except:
            messages.error(self.request, "Unknown Error")
            config = {}

        context.update({
            'config_json': json.dumps(config, indent=4),
        })
        return context
