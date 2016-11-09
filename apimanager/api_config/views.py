# -*- coding: utf-8 -*-

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView


CONFIG = {
    'versions_disabled': ', '.join(['1.4.0', '2.0.0']),
    'functions_disabled': ', '.join([
        'getBank', 'getBanks', 'getAccounts', 'getAccount',
        'getTransactions', 'getTransaction'
    ]),
    'host': 'http://127.0.0.1:8080',
}



class IndexView(LoginRequiredMixin, TemplateView):
    template_name = "api_config/index.html"

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context.update({
            'config': CONFIG,
        })
        return context
