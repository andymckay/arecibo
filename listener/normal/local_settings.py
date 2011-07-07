ARECIBO_PUBLIC_ACCOUNT_NUMBER = "your_public_account_number_here"
ARECIBO_PRIVATE_ACCOUNT_NUMBER = "your_private_account_number_here"

CELERY_ALWAYS_EAGER = True

DEFAULT_FROM_EMAIL = "you.account@gmail.com.that.is.authorized.for.app_engine"
SITE_URL = "http://theurl.to.your.arecibo.instance.com"

ANONYMOUS_ACCESS = True
ANONYMOUS_POSTING = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': '/tmp/arecibo.db',                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

SECRET_KEY = ''
