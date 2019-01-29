# -*- coding: utf-8 -*-
"""
Views for OBP app
"""


import hashlib

from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.urls import reverse
from django.views.generic import RedirectView, FormView

from .api import API, APIError
from .authenticator import AuthenticatorError
from .forms import DirectLoginForm, GatewayLoginForm
from .oauth import OAuthAuthenticator


class LoginToDjangoMixin(object):
    """Mixin to login to Django from views."""
    def login_to_django(self):
        """
        Logs the user into Django
        Kind of faking it to establish if a user is authenticated later on
        """
        api = API(self.request.session.get('obp'))
        try:
            data = api.get('/users/current')
        except APIError as err:
            messages.error(self.request, err)
        except:
            messages.error(self.request, 'Unknown Error')
            return False
        else:
            userid = data['user_id'] or data['email']
            username = hashlib.sha256(userid.encode('utf-8')).hexdigest()
            password = username
            user, _ = User.objects.get_or_create(
                username=username, password=password,
            )
            login(self.request, user)
            return True


class OAuthInitiateView(RedirectView):
    """View to initiate OAuth session"""

    def get_callback_uri(self, request):
        """
        Gets the callback URI to where the user shall be returned after
        initiation at OAuth server
        """
        base_url = '{}://{}'.format(
            request.scheme, request.environ['HTTP_HOST'])
        uri = base_url + reverse('oauth-authorize')
        if 'next' in request.GET:
            uri = '{}?next={}'.format(uri, request.GET['next'])
        return uri

    def get_redirect_url(self, *args, **kwargs):
        callback_uri = self.get_callback_uri(self.request)
        try:
            authenticator = OAuthAuthenticator()
            authorization_url = authenticator.get_authorization_url(
                callback_uri)
        except AuthenticatorError as err:
            messages.error(self.request, err)
            return reverse('home')
        except:
            messages.error(self.request, 'Unknown Error')
            return reverse('home')
        else:
            self.request.session['obp'] = {
                'authenticator': 'obp.oauth.OAuthAuthenticator',
                'authenticator_kwargs': {
                    'token': authenticator.token,
                    'secret': authenticator.secret,
                }
            }
            return authorization_url


class OAuthAuthorizeView(RedirectView, LoginToDjangoMixin):
    """View to authorize user after OAuth 1 initiation"""

    def get_redirect_url(self, *args, **kwargs):
        session_data = self.request.session.get('obp')
        authenticator_kwargs = session_data.get('authenticator_kwargs')
        authenticator = OAuthAuthenticator(**authenticator_kwargs)
        authorization_url = self.request.build_absolute_uri()
        try:
            authenticator.set_access_token(authorization_url)
        except AuthenticatorError as err:
            messages.error(self.request, err)
        except:
            messages.error(self.request, 'Unknown Error')
        else:
            session_data['authenticator_kwargs'] = {
                'token': authenticator.token,
                'secret': authenticator.secret,
            }
            self.login_to_django()
            messages.success(self.request, 'OAuth login successful!')
        redirect_url = self.request.GET.get('next', reverse('home'))
        return redirect_url


class DirectLoginView(FormView, LoginToDjangoMixin):
    """View to login via DirectLogin"""
    form_class = DirectLoginForm
    template_name = 'obp/directlogin.html'

    def get_success_url(self):
        messages.success(self.request, 'DirectLogin successful!')
        redirect_url = self.request.GET.get('next', reverse('home'))
        return redirect_url

    def form_valid(self, form):
        """
        Stores a DirectLogin token in the request's session for use in
        future requests. It also logs in to Django.
        """
        authenticator = form.cleaned_data['authenticator']
        self.request.session['obp'] = {
            'authenticator': 'obp.directlogin.DirectLoginAuthenticator',
            'authenticator_kwargs': {
                'token': authenticator.token,
            }
        }
        self.login_to_django()
        return super(DirectLoginView, self).form_valid(form)


class GatewayLoginView(FormView, LoginToDjangoMixin):
    """View to login via GatewayLogin"""
    form_class = GatewayLoginForm
    template_name = 'obp/gatewaylogin.html'

    def get_success_url(self):
        messages.success(self.request, 'GatewayLogin successful!')
        redirect_url = self.request.GET.get('next', reverse('home'))
        return redirect_url

    def form_valid(self, form):
        """
        Stores a GatewayLogin token in the request's session for use in
        future requests. It also logs in to Django.
        """
        authenticator = form.cleaned_data['authenticator']
        self.request.session['obp'] = {
            'authenticator': 'obp.gatewaylogin.GatewayLoginAuthenticator',
            'authenticator_kwargs': {
                'token': authenticator.token,
            }
        }
        self.login_to_django()
        return super(GatewayLoginView, self).form_valid(form)


class LogoutView(RedirectView):
    """View to logout"""

    def get_redirect_url(self, *args, **kwargs):
        logout(self.request)
        if 'obp' in self.request.session:
            del self.request.session['obp']
        return reverse('home')
