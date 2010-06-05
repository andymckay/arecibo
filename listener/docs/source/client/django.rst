Sample Django Client
=========================================
This is a specific Arecibo installation for Django.

Installation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Check out the Rails client from git.

Place *clients/trunk/django* into project your Django application, or anywhere on the path that Django can find it.

Configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Add the following to settings.py::

ARECIBO_PUBLIC_ACCOUNT_NUMBER = "yourpublicaccountnumber"

There are two ways to send errors to Arecibo. You can either add in some middleware or add to your custom error handlers. If you do both you'll likely end up posting everything twice.

Adding to your middleware
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Django has a middleware layer to handle errors from views. This means that url routing errors (for example) that do not reach a view, do not get processed. Add in the following line to the middleware in Django::

    arecibo.middleware.AreciboMiddleware

So that it would look something like this::

    MIDDLEWARE_CLASSES = (
      'django.middleware.common.CommonMiddleware',
      'django.contrib.sessions.middleware.SessionMiddleware',
      'django.contrib.auth.middleware.AuthenticationMiddleware', 
      'arecibo.middleware.AreciboMiddleware',
    )
    
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
    from arecibo.wrapper import post

    def application_error(request):                     
        t = loader.get_template('500.html')
        uid = post(request, 500)
        c = RequestContext(request, {"uid": uid})
        return HttpResponse(t.render(c), status=500)

In your 500.html template, you'll now have access to the UID that was posted to Arecibo if you'd like to display that to users.

Other times
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can send an error to Arecibo at pretty much any time, for example if you need to capture an error in a view. You can just call the post method and pass through the request.

Notes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* By default we set all 404 as priority 5, 500 as priority 1 and the rest as priority 3. This can be altered in the wrapper.py module.

* The Django documentation does suggest that a 500 may not be rendered and this is true, some errors will be catastrophically bad and prevent a page being returned, but if we can, we can give some response.

* The following errors will be set automatically: url, ip, traceback, type, msg, status, uid and user_agent.