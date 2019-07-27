from BDonor.settings.common import *
from decouple import config, Csv

SECRET_KEY = config('SECRET_KEY')
DEBUG = True
TEMPLATE_DEBUG = DEBUG
ALLOWED_HOSTS = ['bdonor.pythonanywhere.com']
EMAIL_BACKEND = config('EMAIL_BACKEND', default='')
EMAIL_HOST = config('EMAIL_HOST', default='localhost')
EMAIL_PORT = config('EMAIL_PORT', default=25, cast=int)
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=False, cast=bool)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': config('DB_NAME_PAW'),
        'USER': config('DB_USER_PAW'),
        'PASSWORD': config('DB_PASSWORD_PAW'),
        'HOST': config('DB_HOST_PAW'),
        'PORT': '',
        'OPTIONS': {
            'charset': 'utf8mb4',
            'autocommit': True,
            'use_unicode': True,
            'init_command': 'SET storage_engine=INNODB,character_set_connection=utf8mb4,collation_connection=utf8mb4_unicode_ci',
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'"
        },
    }
}

# Static Files
STATIC_URL = '/static/'
MEDIA_URL = '/media/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static_proj'),
]
# STATIC_ROOT = os.path.join('static_cdn', 'static_root')
# MEDIA_ROOT = os.path.join('static_cdn', 'media_root')

# ======== Place It in PythonAnyWhere Static Files Section =======
STATIC_ROOT = '/home/bdonor/static_cdn/static_root'
MEDIA_ROOT = '/home/bdonor/static_cdn/media_root'

# ==================== Security Modules ===================
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_SAMESITE = 'Strict'
SESSION_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
X_FRAME_OPTIONS = 'DENY'
# set low, but when site is ready for deployment, set to at least 15768000 (6 months)
SECURE_HSTS_SECONDS = 300
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Neededf for CorsHeader (accept connections from everywhere)
# CORS_ORIGIN_ALLOW_ALL = True

CORS_ALLOW_HEADERS = (
    'x-requested-with',
    'content-type',
    'accept',
    'origin',
    'authorization',
    'x-csrftoken',
    'token',
    'x-device-id',
    'x-device-type',
    'x-push-id',
    'dataserviceversion',
    'maxdataserviceversion'
)
CORS_ALLOW_METHODS = (
    'GET',
    'POST',
    'PUT',
    'PATCH',
    'DELETE',
    'OPTIONS'
)


CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            # "hosts": [("localhost", 6379)],
            # Production Mode
            "hosts": [os.environ.get('REDIS_URL', 'redis://localhost:6379')],
        },
    },
}
