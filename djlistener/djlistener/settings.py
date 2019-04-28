import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = '171$o7z&zwqhet96y-6#mhjytqn3=-nv%s!^b13jam1a^)y@g#'
DEBUG = False
ALLOWED_HOSTS = []


# Application definition
INSTALLED_APPS = [
    'django.contrib.staticfiles',
    'channels',
    'djlistener',
]

MIDDLEWARE = [
]

ROOT_URLCONF = 'djlistener.urls'
ASGI_APPLICATION = "djlistener.routing.application"

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
            ],
        },
    },
]

#WSGI_APPLICATION = 'djlistener.wsgi.application'
AUTH_USER_MODEL = None


STATIC_URL = '/static/'
STATIC_ROOT = os.path.abspath(os.path.join(BASE_DIR, '..', '..', 'public', 'static'))
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

#
# REDIS_URL
#

#redis://arbitrary_usrname:password@ipaddress:6379/0
REDIS_URL = os.environ.get('REDIS_URL', 'redis://localhost:6379/0')


#
# Channel layer definitions
# http://channels.readthedocs.io/en/latest/topics/channel_layers.html
#

CHANNEL_LAYERS = {
    "default": {
        # This example app uses the Redis channel layer implementation channels_redis
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [REDIS_URL, ],
        },
    },
}

SINEWAVE_CHANNEL_NAME = 'sinewave'

try:
    from .local_settings import *
    print('Using local settings from file "local_settings.py"')
except:
    pass

