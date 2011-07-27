Sample Django Client
=========================================
This is a specific Arecibo installation for Django.

Installation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Install django_arecibo from pypi::

    pip install django_arecibo

This will pull down the arecibo library as well.

Configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Add the following to settings.py::

    ARECIBO_PUBLIC_ACCOUNT_NUMBER = "yourpublicaccountnumber"
    ARECIBO_SERVER_URL = "http://url.to.your.server"

Optionally if you want to use email::

    ARECIBO_SERVER_EMAIL = "email@to.your.server"

Emailing in errors is currently only supported by the App Engine server.

There are two ways to send errors to Arecibo. You can either add in some middleware or add to your custom error handlers. If you do both you'll likely end up posting everything twice.

Adding to your middleware
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Django has a middleware layer to handle errors from views. This means that url routing errors 404's (for example) that do not reach a view, do not get processed. Add in the following line to the middleware in Django::

    django_arecibo.middleware.AreciboMiddleware

So that it would look something like this::

    MIDDLEWARE_CLASSES = (
      'django.middleware.common.CommonMiddleware',
      'django.contrib.sessions.middleware.SessionMiddleware',
      'django.contrib.auth.middleware.AuthenticationMiddleware',
      'django_arecibo.middleware.AreciboMiddleware',
    )

One *disadvantage* of the middleware is that it means your unit tests will raise errors. It's also slightly harder to customise, unless you write your own middleware.

Adding to your custom views
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Django has a 404 or 500 error handler that can be overridden. We can use this to post to Arecibo, for example here's a standard 500 error handler::

    from django.template import RequestContext, loader
    from django.http import HttpResponse

    def application_error(request):
        t = loader.get_template('500.html')
        c = RequestContext(request)
        return HttpResponse(t.render(c), status=500)

Add into this your post to Arecibo so it reads::

    from django.template import RequestContext, loader
    from django.http import HttpResponse
    from django_arecibo.wrapper import post

    def application_error(request):
        t = loader.get_template('500.html')
        uid = post(request, 500)
        c = RequestContext(request, {"uid": uid})
        return HttpResponse(t.render(c), status=500)

This is relatively easy to do since, you'll be writing a handler 500 anyway. Feel free to customize your data to send through different priorities etc. In your 500.html template, you'll now have access to the UID that was posted to Arecibo if you'd like to display that to users.


Using celery
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can use celery to delay the posting of Arecibo so that your error page is not dependent upon the Arecibo request. To use a celery version of post, change the following::

    from django_arecibo.wrapper import post

To::

    from django_arecibo.tasks import post

You must add the following to your Django settings.py so that Celery will correctly import the task::

    CELERY_IMPORTS = ('django_arecibo.tasks',)

If you are using middleware, you can do this by using instead::

    'django_arecibo.middleware.AreciboMiddlewareCelery'

Further configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can pass through an extra configuration dictionary for filtering or excluding variables posted to Arecibo. For example, if you have a field "password" in your site and you don't want this ever posted to Arecibo, you can exclude this::

    ARECIBO_SETTINGS = {
        'EXCLUDED_POST_VARS': ['password',],
    }

The options are:

* EXCLUDED_POST_VARS - a list of the fields you'd like not to post to Arecibo

* EXCLUDED_FILES - a list of the files you'd like not to send information about to Arecibo

* FILTERED_POST_VARS - instead of sending the value of the field, sends * instead

* FILTERED_FILES -  instead of sending information about the file, sends * instead

Other times
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can send an error to Arecibo at pretty much any time, for example if you need to capture an error in a view. You can just call the post method and pass through the request.

Notes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* By default we set all 404 as priority 5, 500 as priority 1 and the rest as priority 3. This can be altered in the wrapper.py module.

* The Django documentation does suggest that a 500 may not be rendered. It is conceivable that your error could be so bad that Arecibo never gets called. For example you could be losing network connections or something worse like a syntax error. In this case not much can save you.

* The following errors will be set automatically: url, ip, traceback, type, msg, status, uid and user_agent.
