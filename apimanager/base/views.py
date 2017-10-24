# -*- coding: utf-8 -*-
"""
Views for base app
"""

from django.conf import settings
from django.views.generic import TemplateView


class HomeView(TemplateView):
    """View for home page"""
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['API_HOST'] = settings.API_HOST
        return context
