import os
import sys

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ROOT_PATH = os.path.abspath(os.path.dirname(__file__))

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': '/Users/andy/tempy/db.sql',                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

TIME_ZONE = 'UTC'

LANGUAGE_CODE = 'en-us'

SITE_ID = 1

USE_I18N = False
MEDIA_ROOT = ''
MEDIA_URL = ''


# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'userstorage.middleware.UserStorage',
    'app.middleware.Middleware'
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'app.context.context',
)

ROOT_URLCONF = 'urls'

TEMPLATE_DIRS = (
    os.path.join(ROOT_PATH, 'templates'),
    os.path.join(ROOT_PATH, 'custom', 'templates')
)

SETTINGS_MODULE = 'settings'
INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.admin',
    'error',
    'app',
    'notifications',
    'receiving',
    'users',
    'projects',
    'custom',
    'djcelery'
)

LOGIN_URL = '/login/'
LOGOUT_URL = '/logout/'
LOGIN_REDIRECT_URL = '/list/'

TEST_RUNNER = "app.test_runner.AreciboRunner"
ARECIBO_PUBLIC_ACCOUNT_NUMBER = "your_public_account_number_here"
ARECIBO_PRIVATE_ACCOUNT_NUMBER = "your_private_account_number_here"

DEFAULT_FROM_EMAIL = "you.account@gmail.com.that.is.authorized.for.app_engine"
SITE_URL = "http://theurl.to.your.arecibo.instance.com"

ANONYMOUS_ACCESS = False

CELERY_RESULT_BACKEND = "amqp"

CELERY_IMPORTS = ("custom", "users", "notifications", "receiving.post", )

BROKER_HOST = "localhost"
BROKER_PORT = 5672
BROKER_USER = "guest"
BROKER_PASSWORD = "guest"
BROKER_VHOST = ""

try:
    from local_settings import *
except ImportError:
    pass

# Add in required lib.
lib = os.path.abspath(os.path.join(ROOT_PATH, '..', 'lib'))

assert os.path.exists(lib), 'Cannot find required lib directory at: %s' % lib
if lib not in sys.path:
    sys.path.append(lib)
