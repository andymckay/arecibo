# Copyright 2008 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Django settings for google-app-engine-django project.

import os

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

DATABASE_ENGINE = 'appengine'  # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_NAME = ''             # Or path to database file if using sqlite3.
DATABASE_USER = ''             # Not used with sqlite3.
DATABASE_PASSWORD = ''         # Not used with sqlite3.
DATABASE_HOST = ''             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.
TIME_ZONE = 'UTC'

LANGUAGE_CODE = 'en-us'

SITE_ID = 1

USE_I18N = False
MEDIA_ROOT = ''
MEDIA_URL = ''


# Make this unique, and don't share it with anybody.
SECRET_KEY = 'hvhdrfgd4tg54lwi435qa4tg.isz6taz^%sg_nx'

# Ensure that email is not sent via SMTP by default to match the standard App
# Engine SDK behaviour. If you want to sent email via SMTP then add the name of
# your mailserver here.
EMAIL_HOST = ''

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'appengine_django.auth.middleware.AuthenticationMiddleware'
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'app.context.context',
)

ROOT_URLCONF = 'urls'

ROOT_PATH = os.path.dirname(__file__)
TEMPLATE_DIRS = (
    os.path.join(ROOT_PATH, 'templates')
)

INSTALLED_APPS = (
     'django.contrib.auth',
     'appengine_django',
     'appengine_django.auth',
     'error',
     'app',
     'notifications',
     'receiving',
     'custom'
)

try:
    from local_settings import *
except ImportError:
    pass