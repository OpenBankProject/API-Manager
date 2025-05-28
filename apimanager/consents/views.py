# -*- coding: utf-8 -*-
"""
Views of consent requests app
"""

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, RedirectView, View
from obp.api import API, APIError
from base.filters import BaseFilter, FilterTime
from datetime import datetime
from django.conf import settings
from django.urls import reverse
from django.http import HttpResponseRedirect
from apimanager.settings import UNDEFINED



class IndexView(LoginRequiredMixin, TemplateView):
    """Index view for consent requests"""
    template_name = "consents/index.html"

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        consents = []
        api = API(self.request.session.get('obp'))
        try:
            urlpath = '/my/consents'
            consents = api.get(urlpath, settings.API_VERSION['v510'])
            if 'code' in consents and consents['code']>=400:
                messages.error(self.request, consents['message'])
                consents = []
            else:
                consents = consents['consents']
        except APIError as err:
            messages.error(self.request, err)
        except Exception as err:
            messages.error(self.request, err)

        context.update({
            'consents': consents,
        })
        return context

class RevokeConsents(LoginRequiredMixin, View):
    """View to revoke a consent"""

    def post(self, request, *args, **kwargs):
        """Deletes consent from API"""
        api = API(self.request.session.get('obp'))
        try:
            consent_id= kwargs['consent_id']
            urlpath = '/my/consents/{}'.format(consent_id)
            response = api.delete(urlpath, settings.API_VERSION['v510'])
            if 'code' in response and response['code'] >= 400:
                messages.error(self.request, response['message'])
            else:
                msg = 'Consent {} has been deleted.'.format(consent_id)
                messages.success(request, msg)
        except APIError as err:
            messages.error(request, err)
        except Exception as err:
            messages.error(self.request, err)

        return HttpResponseRedirect(reverse('consents-index'))