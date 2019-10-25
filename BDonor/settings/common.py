
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
    'widget_tweaks',
    'django_cleanup',
    # 'django_cool_paginator',
    'el_pagination',
    'django_extensions',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.facebook',
    # 'corsheaders',
    'rest_framework',
    'channels',
    'ckeditor',
    'ckeditor_uploader',
    'django_social_share',
    'django_countries',
    'multiselectfield',
    # --- Local Apps ---
    'accounts',
    'utils',
    'suspicious',
    'chat',
    'donations',
    'stripe',
    'priceplan',
    'checkout',
    'donationBank',
    'blog',
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
    # Custom Middlewares
    'middlewares.middlewares.RequestMiddleware',
]

ROOT_URLCONF = 'BDonor.urls'
ASGI_APPLICATION = "BDonor.routing.application"

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

WSGI_APPLICATION = 'BDonor.wsgi.application'

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


from BDonor.settings.third_party_configs import *

# stripe
STRIPE_PUBLISHABLE_KEY = config('STRIPE_PUBLISHABLE_KEY')
STRIPE_SECRET_KEY = config('STRIPE_SECRET_KEY')

# Custom for Stripe by Numan
# if DEBUG:
#     STRIPE_PUBLISHABLE_KEY = ''
#     STRIPE_SECRET_KEY = ''

# else:
#     STRIPE_PUBLISHABLE_KEY = ''
#     STRIPE_SECRET_KEY = ''
