"""
Django settings for hh project.
"""
import os
from datetime import timedelta
import psycopg2

# Local settings
try:
    from hh.local_settings import *
except ImportError:
    pass

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Application definition
INSTALLED_APPS = [
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'django.contrib.flatpages',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.facebook',
    'allauth.socialaccount.providers.google',
    #'allauth.socialaccount.providers.instagram',
    'allauth.socialaccount.providers.twitter',
    'allauth.socialaccount.providers.vk',
    #'allauth.socialaccount.providers.mailru',
    'widget_tweaks',
    'django_extensions',
    'debug_toolbar',
    'stronghold',
    'crispy_forms',
    'sitetree',
    'compressor',
    'avatar',
    'cities_light',
    'reversion',
    'django_select2',
    'colorful',
    'geoposition',
    'imagekit',
    'envelope',

    # HH apps
    'hh',
    'users',
    'booking',
    'hotels',
    'payments'
]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'hh.middleware.UserMiddleware',
    'hh.middleware.AdminLocaleMiddleware',
    'hh.middleware.WhodidMiddleware',
    'stronghold.middleware.LoginRequiredMiddleware',
    'booking.middleware.IncomingOrdersMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware'
]

ROOT_URLCONF = 'hh.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'hh/templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

SITE_ID = 1

LOCALE_PATHS = (
    os.path.join(os.path.dirname(__file__), "locale"),
    os.path.join(os.path.dirname(__file__), "app_locale"),
)

WSGI_APPLICATION = 'hh.wsgi.application'

# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

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

# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'ru'
LANGUAGES = (('ru', 'Russian'), ('en', 'English'),)

ADMIN_LANGUAGE_CODE = 'en-US'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_URL = '/static/'
MEDIA_URL = '/media/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'hh/static'),
    os.path.join(BASE_DIR, 'bower_components'),
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder'
)

FIXTURE_DIRS = (
    os.path.join(BASE_DIR, 'fixtures'),
)

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
        'TIMEOUT': 600
    },
    'select2': {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

LOGIN_REDIRECT_URL = '/'

EMAIL_SUBJECT_PREFIX = '[HostelHunt] '

# Logs
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt': "%d/%b/%Y %H:%M:%S"
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'var/logs/hh.log',
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'hh': {
            'handlers': ['file'],
            'level': 'DEBUG',
        },
    }
}

# Django stronghold
STRONGHOLD_DEFAULTS = True

STRONGHOLD_PUBLIC_URLS = (
    r'^/admin.+$',
    r'^/accounts.+$',
    r'^/__debug__.+$',
    r'^/payments/check/payment$',
    r'^/select2/fields/auto.+$',
    r'^/booking/search.+$',
    r'^/pages/contacts.+$',
    r'^/$'
)

# Django avatar
AVATAR_GRAVATAR_DEFAULT = 'mm'
AVATAR_AUTO_GENERATE_SIZES = (24, 25, 160)
AVATAR_MAX_AVATARS_PER_USER = 5

# Django allauth
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 1
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
ACCOUNT_USERNAME_MIN_LENGTH = 3
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_PASSWORD_MIN_LENGTH = 8
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = True

# Django crispy forms
CRISPY_TEMPLATE_PACK = 'bootstrap3'

# Django sitetree
SITETREE_MODEL_TREE_ITEM = 'hh.SiteTreeItem'
SITETREE_MODEL_TREE = 'hh.SiteTreeTree'

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

# Django cities-light
CITIES_LIGHT_TRANSLATION_LANGUAGES = ['ru']
CITIES_LIGHT_INCLUDE_COUNTRIES = ['RU']
CITIES_LIGHT_APP_NAME = 'hh'

# Celery
BROKER_URL = 'redis://localhost:6379'
CELERY_RESULT_BACKEND = 'redis://localhost:6379'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Europe/Moscow'
CELERYBEAT_SCHEDULE = {
    'close_old_orders': {
        'task': 'booking.tasks.close_old_orders',
        'schedule': timedelta(seconds=60)
    },
}

# Django phonenumber
PHONENUMBER_DB_FORMAT = 'NATIONAL'
PHONENUMBER_DEFAULT_REGION = 'RU'

# Django select2
SELECT2_CACHE_BACKEND = 'select2'
SELECT2_JS = 'AdminLTE/plugins/select2/select2.full.min.js'
SELECT2_CSS = 'AdminLTE/plugins/select2/select2.min.css'

# Django geoposition
GEOPOSITION_MAP_WIDGET_HEIGHT = 300

# Django envelope
ENVELOPE_EMAIL_RECIPIENTS = ADMINS
ENVELOPE_SUBJECT_INTRO = 'Новое сообщение от пользователя. '

# HH settings
HH_SEARCH_RESULTS_PER_PAGE = 30
HH_BOOKING_MAX_ORDER_ROOMS = 5
HH_BOOKING_ORDER_LIFETIME = 30  # in minutes
HH_BOOKING_ORDER_USER_LIMIT = 1
HH_BOOKING_ORDER_PARTNER_LIMIT = 3
HH_BOOKING_ORDER_TIME_LIMIT = 1  # in minutes

