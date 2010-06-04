App Engine Installation
====================================

Requirements
----------------------------

You will require a App Engine application. You can create a free one at http://appengine.google.com/.

So you can push to to the server you will need a copy of the **Python** App Engine SDK installed, you can get that here: http://code.google.com/appengine/downloads.html#Google_App_Engine_SDK_for_Python

You will need git to check out Arecibo from github: http://git-scm.com/

You will need the current version of Django. At the time of writing, we are supporting Django 1.2.1: http://www.djangoproject.com/download/1.2.1/tarball/ - the chances are any later version will work.

Installation steps
------------------------------------------------

The following are done on Mac OS X. Other operating system may vary.

1. Create an App Engine instance
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

At http://appengine.google.com/ create a new App Engine application. Give your new App Engine installation a unique name. This is the **app name** that we will be using in later steps.

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

3. Configure Arecibo
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

There are at least two things you will need to change: the *app.yaml* file and *local_settings.py* file. There are examples of each of these files in the app_engine, directory. The backup version of these files need to be copied and changed.

First *app.yaml*::

    ~ $ cd arecibo/listener/app_engine
    ~/arecibo/listener/app_engine $ cp app.yaml.example app.yaml

Alter the first line of *app.yaml*::

    application: your_application_error

Replacing *your_application_error* with the unique name of your application from step 1.

Second *local_settings.py*::

    ~/arecibo/listener/app_engine $ cp local_settings.py.example local_settings.py
    
Then alter the file as detailed::

    ARECIBO_PUBLIC_ACCOUNT_NUMBER = "your_public_account_number_here"
    ARECIBO_PRIVATE_ACCOUNT_NUMBER = "your_private_account_number_here"

    DEFAULT_FROM_EMAIL = "you.account@gmail.com.that.is.authorized.for.app_engine"
    SITE_URL = "http://theurl.to.your.arecibo.instance.com"
    
Line 1: ARECIBO_PUBLIC_ACCOUNT_NUMBER should be a unique id that you'll be using to post to your site. This can be anything you like. Normally a random string 32 characters long.

Line 2: ARECIBO_PRIVATE_ACCOUNT_NUMBER should be a unique id that you'll be using to read from your site. This can be anything you like. Normally a random string 32 characters long.

Line 3: DEFAULT_FROM_EMAIL is the Google email address you used to setup your App Engine site. This has to be an email that is authorized by App Engine, the simplest is to use the one you created you site with.

Line 4: SITE_URL the full URL (including protocol) that your site is at.

An example file might be::

    ARECIBO_PUBLIC_ACCOUNT_NUMBER = "wetlwk36524352345y.rutywr5hs.tgywq43w5jy2w35"
    ARECIBO_PRIVATE_ACCOUNT_NUMBER = "swtqak365qkt6qo45tyh45tq3k5w345qhtr2q75y2"

    DEFAULT_FROM_EMAIL = "some.user@googlemail.com"
    SITE_URL = "http://my-arecibo-site.appspot.com"

4. Copy over Django
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Download and copy over Django so we can be sure we use the version of Django that is compatible, not the the one that comes by default::

    ~/arecibo/listener/app_engine $ wget http://media.djangoproject.com/releases/1.2/Django-1.2.1.tar.gz
    ..
    ~/arecibo/listener/app_engine $ tar zxf Django-1.2.1.tar.gz 
    ~/arecibo/listener/app_engine $ mv Django-1.2.1/django .
    ~/arecibo/listener/app_engine $ rm -rf Django-1.2.1*
    
5. Upload to App Engine
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you don't have the **Python** App Engine SDK you will need to install it at this point.

Uploading to App Engine is a simple as:

    ~/arecibo/listener/app_engine $ appcfg.py update .

Follow the prompts for your email and password. You should see quite a few messages scroll past. If you get this message at the end, then it's worked and you should be able to visit the site in your browser.::

    Checking if new version is ready to serve.
    Closing update: new version is ready to start serving.
    Uploading index definitions.
    Uploading cron entries
