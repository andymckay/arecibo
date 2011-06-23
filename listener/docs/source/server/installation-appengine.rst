Installation (App Engine)
====================================

The App Engine installation of Arecibo is no longer recommended and will not be updated. It still works just fine, but I'm not maintaining it. Hopefully someone else will.

Requirements
----------------------------

You will require a App Engine application. These are free to create, or you can run one locally to test. To deploy an instance of Arecibo to App Engine you will need a copy of the App Engine SDK. You will need the *Python* version of the App Engine SDK [1]_.

You will need git to check out Arecibo from github [2]_.

You will need the current version of Django. At the time of writing, we are supporting Django 1.2.3 [3]_.

Installation steps
------------------------------------------------

The following steps are done on Mac OS X. Other operating systems may vary.

1 a. Create an App Engine instance
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

At http://appengine.google.com/ create a new App Engine application. Give your new App Engine installation a unique name. This is the **app name** that you will be using in later steps.

1 b. Install the Google App Engine SDK
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Install the Google App Engine SDK. If you already have it installed, you can skip this step.

2. Download Arecibo
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Run the following command::

    ~ $ git clone git://github.com/andymckay/arecibo.git
    Initialized empty Git repository in /Users/andy/arecibo/.git/
    remote: Counting objects: 601, done.
    remote: Compressing objects: 100% (511/511), done.
    remote: Total 601 (delta 233), reused 209 (delta 40)
    Receiving objects: 100% (601/601), 260.74 KiB | 275 KiB/s, done.
    Resolving deltas: 100% (233/233), done.

3 a. Configure Arecibo (easy way)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Run create.py and follow the prompts::

    ~ $ cd arecibo
    ~/arecibo $ python configure.py

3 b. Configure Arecibo (manual way)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

There are at least two things you will need to change: the *app.yaml* file and *local_settings.py* file. There are examples of each of these files in the app_engine, directory. The backup version of these files need to be copied and changed.

First *app.yaml*::

    ~ $ cd arecibo/listener/app_engine
    ~/arecibo/listener/app_engine $ cp app.yaml.example app.yaml

Alter the first line of *app.yaml*::

    application: your_application_error

Replacing *your_application_error* with the **app name** of your application from step 1.

Second *local_settings.py*::

    ~/arecibo/listener/app_engine $ cp local_settings.py.example local_settings.py

Then alter the file as detailed::

    ARECIBO_PUBLIC_ACCOUNT_NUMBER = "your_public_account_number_here"
    ARECIBO_PRIVATE_ACCOUNT_NUMBER = "your_private_account_number_here"

    DEFAULT_FROM_EMAIL = "you.account@gmail.com.that.is.authorized.for.app_engine"
    SITE_URL = "http://theurl.to.your.arecibo.instance.com"

The variables ARECIBO_PUBLIC_ACCOUNT_NUMBER and ARECIBO_PRIVATE_ACCOUNT_NUMBER should be unique id that you'll be using to post to your site. This is used in URLs, so try to avoid / and unicode, any combination of 32 letters and numbers normally works.

DEFAULT_FROM_EMAIL is the Google email address you used to setup your App Engine site. This has to be an email that is authorized by App Engine, the simplest is to use the one you created your App Engine site with. For documentation on how to send email from App Engine, see here: http://code.google.com/appengine/docs/python/mail/

SITE_URL the full URL (including protocol) that your site is at.

An example file might be::

    ARECIBO_PUBLIC_ACCOUNT_NUMBER = "wetlwk36524352345y.rutywr5hs.tgywq43w5jy2w35"
    ARECIBO_PRIVATE_ACCOUNT_NUMBER = "swtqak365qkt6qo45tyh45tq3k5w345qhtr2q75y2"

    DEFAULT_FROM_EMAIL = "some.user@googlemail.com"
    SITE_URL = "http://my-arecibo-site.appspot.com"

Download and copy over Django (this is not included for licensing reasons). Then we can be sure we use the version of Django that is compatible, not the the one that comes by default with App Engine::

    ~/arecibo/listener/app_engine $ wget http://media.djangoproject.com/releases/1.2/Django-1.2.1.tar.gz
    ..
    ~/arecibo/listener/app_engine $ tar zxf Django-1.2.1.tar.gz
    ~/arecibo/listener/app_engine $ mv Django-1.2.1/django .
    ~/arecibo/listener/app_engine $ rm -rf Django-1.2.1*

4. Upload to App Engine
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you don't have the **Python** App Engine SDK you will need to install it at this point.

Uploading to App Engine is a simple as::

    ~/arecibo/listener/app_engine $ appcfg.py update .

Follow the prompts for your email and password. You should see quite a few messages scroll past. If you get these messages at the end, then it's worked and you should be able to visit the site in your browser::

    Checking if new version is ready to serve.
    Closing update: new version is ready to start serving.
    Uploading index definitions.
    Uploading cron entries

.. [1] http://code.google.com/appengine/downloads.html#Google_App_Engine_SDK_for_Python

.. [2] http://git-scm.com/

.. [3] http://www.djangoproject.com/download/1.2.1/tarball/