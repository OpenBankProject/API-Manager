# -*- coding: utf-8 -*-
"""
Views for OAuth 1 app
"""

import hashlib

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.urls import reverse
from django.views.generic import RedirectView

from requests_oauthlib import OAuth1Session
from requests_oauthlib.oauth1_session import TokenRequestDenied

from base.api import api


class InitiateView(RedirectView):
    """View to initiate OAuth 1 session"""

    def get_callback_uri(self, request):
        """
        Gets the callback URI to where the user shall be returned after
        authorization at OAuth 1 server
        """
        base_url = '{}://{}'.format(
            request.scheme, request.environ['HTTP_HOST'])
        uri = base_url + reverse('oauth-authorize')
        if 'next' in request.GET:
            uri = '{}?next={}'.format(uri, request.GET['next'])
        return uri

    def get_redirect_url(self, *args, **kwargs):
        callback_uri = self.get_callback_uri(self.request)
        session = OAuth1Session(
            settings.OAUTH_CONSUMER_KEY,
            client_secret=settings.OAUTH_CONSUMER_SECRET,
            callback_uri=callback_uri,
        )

        try:
            url = settings.OAUTH_API + settings.OAUTH_TOKEN_PATH
            response = session.fetch_request_token(url)
        except (ValueError, TokenRequestDenied) as err:
            messages.error(self.request, err)
            return reverse('home')

        url = settings.OAUTH_API + settings.OAUTH_AUTHORIZATION_PATH
        authorization_url = session.authorization_url(url)
        self.request.session['oauth_token'] = response.get('oauth_token')
        self.request.session['oauth_secret'] = response.get('oauth_token_secret')
        self.request.session.modified = True
        return authorization_url


class AuthorizeView(RedirectView):
    """View to authorize user"""

    def login_to_django(self):
        """
        Logs the user into Django
        Kind of faking it to establish if a user is authenticated later on
        """
        data = api.get(self.request, '/users/current')
        userid = data['user_id'] or data['email']
        username = hashlib.sha256(userid.encode('utf-8')).hexdigest()
        password = username
        user, _ = User.objects.get_or_create(
            username=username, password=password,
        )
        login(self.request, user)

    def get_redirect_url(self, *args, **kwargs):
        session = OAuth1Session(
            settings.OAUTH_CONSUMER_KEY,
            settings.OAUTH_CONSUMER_SECRET,
            resource_owner_key=self.request.session.get('oauth_token'),
            resource_owner_secret=self.request.session.get('oauth_secret')
        )
        session.parse_authorization_response(self.request.build_absolute_uri())
        url = settings.OAUTH_API + settings.OAUTH_ACCESS_TOKEN_PATH
        try:
            response = session.fetch_access_token(url)
        except TokenRequestDenied as err:
            response = {}
            messages.error(self.request, err)

        self.request.session['oauth_token'] = response.get('oauth_token')
        self.request.session['oauth_secret'] = response.get('oauth_token_secret')
        self.login_to_django()
        redirect_url = self.request.GET.get('next', reverse('consumers-index'))
        return redirect_url


class LogoutView(RedirectView):
    """View to logout"""

    def get_redirect_url(self, *args, **kwargs):
        logout(self.request)
        return reverse('home')
