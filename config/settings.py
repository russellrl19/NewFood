import os
import dj_database_url

# begin time zone middleware
# details: https://docs.djangoproject.com/en/2.0/topics/i18n/timezones/#selecting-the-current-time-zone
import pytz

from django.utils import timezone
from django.utils.deprecation import MiddlewareMixin

class TimezoneMiddleware(MiddlewareMixin):
    def process_request(self, request):
        tzname = request.session.get('django_timezone')
        if tzname:
            timezone.activate(pytz.timezone(tzname))
        else:
            timezone.deactivate()

    BASE_URL = "https://giveback.herokuapp.com/"

    DATABASES = { 'default': dj_database_url.config() }

    ALLOWED_HOSTS = [
        u'127.0.0.1',
        u'giveback.herokuapp.com'
    ]

    DEBUG = True

    EMAIL_PORT = 465
    EMAIL_USE_TLS = False
    EMAIL_BACKEND = 'django_smtp_ssl.SSLEmailBackend'

# Email configuration
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'GiveBackFoodServices@gmail.com'
EMAIL_HOST_PASSWORD = os.environ['EMAIL_PASSWORD']

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'b$vbnxkjs!8rzd_)c99#+r=_t9x$sp4&83w7&h9jilicvw2_if'

# Application definition

INSTALLED_APPS = [
    'photosleuth',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
#    'social_django',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


ROOT_URLCONF = 'cwps.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'cwps.wsgi.application'

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'
MEDIA_URL = '/media/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'home/static'),
)

LOGIN_REDIRECT_URL = '/home'

#Django authentication backends
AUTHENTICATION_BACKENDS = {
#    'social_core.backends.facebook.FacebookOAuth2',
    'django.contrib.auth.backends.ModelBackend'
}
