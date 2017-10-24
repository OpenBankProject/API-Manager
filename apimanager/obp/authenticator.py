# -*- coding: utf-8 -*-
"""
Base authenticator for OBP app
"""

import hashlib

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.models import User


class AuthenticatorError(Exception):
    """Exception class for Authenticator errors"""
    pass


class Authenticator(object):
    """Generic authenticator to the API"""
    pass
