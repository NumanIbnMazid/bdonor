
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # --- Third Party Apps ---
    'django_extensions',
    'widget_tweaks',
    'django_cleanup',
    'django_cool_paginator',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.facebook',
    # 'corsheaders',
    'rest_framework',
    'channels',
    # --- Local Apps ---
    'accounts',
    'utils',
    'suspicious',
    'chat',
]

SITE_ID = 1

AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    # 'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
)

SOCIALACCOUNT_PROVIDERS = {'facebook':
                           {'METHOD': 'oauth2',
                            'SCOPE': ['email', 'public_profile', 'user_friends'],
                            'AUTH_PARAMS': {'auth_type': 'reauthenticate'},
                            'INIT_PARAMS': {'cookie': True},
                            'FIELDS': [
                                'id',
                                'email',
                                'name',
                                'first_name',
                                'last_name',
                                'verified',
                                'locale',
                                'timezone',
                                'link',
                                'gender',
                                'updated_time',
                            ],
                            'EXCHANGE_TOKEN': True,
                            'LOCALE_FUNC': lambda request: 'en_US',
                            'VERIFIED_EMAIL': True,
                            'VERSION': 'v2.4'
                            }
                           }

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    # CorsHeader Middleware before CommonMiddleware
    # 'corsheaders.middleware.CorsMiddleware',
    # CorsHeader Middleware
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'BDonar.urls'
ASGI_APPLICATION = "BDonar.routing.application"

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            # 'loaders': [
            #     ('django.template.loaders.cached.Loader', [
            #         'django.template.loaders.filesystem.Loader',
            #         'django.template.loaders.app_directories.Loader',

            #     ]),
            # ],
        },
    },
]

WSGI_APPLICATION = 'BDonar.wsgi.application'

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization - Default
# LANGUAGE_CODE = 'en-us'
# TIME_ZONE = 'UTC'
# USE_I18N = True
# USE_L10N = True
# USE_TZ = True

# Internationalization - Custom
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Dhaka'
USE_I18N = True
USE_L10N = True
USE_TZ = False


# Allauth Staffs
LOGIN_URL = '/account/login/'
LOGOUT_URL = '/'
LOGIN_REDIRECT_URL = '/'
SITE_NAME = 'BDonar'
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 7
ACCOUNT_LOGIN_ATTEMPTS_LIMIT = 5
ACCOUNT_LOGIN_ATTEMPTS_TIMEOUT = 300
ACCOUNT_USERNAME_MIN_LENGTH = 1
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = True
ACCOUNT_SIGNUP_PASSWORD_VERIFICATION = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_LOGOUT_ON_PASSWORD_CHANGE = True
ACCOUNT_SIGNUP_PASSWORD_ENTER_TWICE = True
ACCOUNT_EMAIL_CONFIRMATION_AUTHENTICATED_REDIRECT_URL = '/'
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_VERIFICATION = 'optional'
ACCOUNT_EMAIL_SUBJECT_PREFIX = 'BDonar'
ACCOUNT_USERNAME_BLACKLIST = ['robot', 'hacker', 'virus', 'spam']
ACCOUNT_ADAPTER = 'BDonar.adapter.UsernameMaxAdapter'


# Cool Paginator Staffs
COOL_PAGINATOR_NEXT_NAME = "next"
COOL_PAGINATOR_PREVIOUS_NAME = "previous"
COOL_PAGINATOR_SIZE = "SMALL"
COOL_PAGINATOR_ELASTIC = "300px"


# File Staffs
ALLOWED_IMAGE_TYPES = ['.jpg', '.jpeg', '.png']
# 1.5MB - 1621440
# 2.5MB - 2621440
# 5MB - 5242880
# 10MB - 10485760
# 20MB - 20971520
# 50MB - 5242880
# 100MB 104857600
# 250MB - 214958080
# 500MB - 429916160
MAX_IMAGE_UPLOAD_SIZE = 1621440
