Remote access
==========================================

The instance on Google App Engine can be accessed by using the *remote_api*[1]_. A management command has been added to allow you to do this::

    python manage.py remote
    App Engine interactive console for test-areciboapp
    >>>

You can then execute Python commands. To view the timestamp of the first error::

    >>> Error.all()[0].timestamp
    Username:***********@googlemail.com
    Password:
    datetime.datetime(2010, 6, 14, 16, 25, 49, 835365)

Note that the console is not appropriate for tasks that do a large number of datastore requests, since each is a HTTP request. For example: batch altering of records - for that you'd be better off uploading a specific script.

.. [1] http://code.google.com/appengine/articles/remote_api.html