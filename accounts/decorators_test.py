try:
    from functools import wraps
except ImportError:
    from django.utils.functional import wraps
# from urllib.parse import urlparse

from django.conf import settings
from django.contrib.auth import REDIRECT_FIELD_NAME
# from django.core.exceptions import PermissionDenied
# from django.shortcuts import resolve_url
from django.contrib.auth import logout #parameter (request)
from django.contrib.auth.decorators import user_passes_test




def can_browse_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url=None):
    actual_decorator = user_passes_test(
        lambda u: u.user_permissions_user.can_browse == True,
        login_url=settings.BLOCKED_URL,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


def can_donate_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url=None):
    actual_decorator = user_passes_test(
        lambda u: u.user_permissions_user.can_donate == True,
        login_url=settings.HOME_URL,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


def can_ask_for_a_donor_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url=None):
    actual_decorator = user_passes_test(
        lambda u: u.user_permissions_user.can_ask_for_a_donor == True,
        login_url=settings.HOME_URL,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


def can_manage_bank_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url=None):
    actual_decorator = user_passes_test(
        lambda u: u.user_permissions_user.can_manage_bank == True,
        login_url=settings.HOME_URL,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


def can_chat_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url=None):
    actual_decorator = user_passes_test(
        lambda u: u.user_permissions_user.can_chat == True,
        login_url=settings.HOME_URL,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator
