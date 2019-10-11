from django.contrib.auth.decorators import login_required, user_passes_test
from django.conf import settings


# Browse ability

user_can_browse_required = user_passes_test(
    lambda user: user.user_permissions_user.can_browse == True, login_url=settings.BLOCKED_URL)


def can_browse_required(view_func):
    decorated_view_func = login_required(user_can_browse_required(view_func))
    return decorated_view_func


# Donate ability

user_can_donate_required = user_passes_test(
    lambda user: user.user_permissions_user.can_donate == True, login_url=settings.ACCESS_DENIED_URL)


def can_donate_required(view_func):
    decorated_view_func = login_required(user_can_donate_required(view_func))
    return decorated_view_func

# Donor Request ability


user_can_ask_for_a_donor_required = user_passes_test(
    lambda user: user.user_permissions_user.can_ask_for_a_donor == True, login_url=settings.ACCESS_DENIED_URL)


def can_ask_for_a_donor_required(view_func):
    decorated_view_func = login_required(user_can_ask_for_a_donor_required(view_func))
    return decorated_view_func

# Bank Manage ability


user_can_manage_bank_required = user_passes_test(
    lambda user: user.user_permissions_user.can_manage_bank == True, login_url=settings.ACCESS_DENIED_URL)


def can_manage_bank_required(view_func):
    decorated_view_func = login_required(user_can_manage_bank_required(view_func))
    return decorated_view_func

# Chat ability


user_can_chat_required = user_passes_test(
    lambda user: user.user_permissions_user.can_chat == True, login_url=settings.ACCESS_DENIED_URL)


def can_chat_required(view_func):
    decorated_view_func = login_required(user_can_chat_required(view_func))
    return decorated_view_func
