Posting errors
====================================

This covers the process of posting an error from your website into Arecibo. There main method of sending an error to Arecibo is by a HTTP post. It's easy to add in your own and hopefully more will be made open source.

HTTP Post
---------------------------

The URL for version 1 of the API is:

http://yoursite.com/v/1/

When the next major release of Arecibo API happens, we will increment the URL to /v/2/, leaving the /v/1/ active. This will allow clients to upgrade as needed.

The method for sending an error is simple, a HTTP POST to the above URL containing the variables set out in the documentation.

Notes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* HTTP GET requests will be ignored, only POST

* The only required variable is the Arecibo API key

* If possible set a timeout in your posting client (say 10 seconds)

Example in Python
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In this example we'll use the public test site:

* URL: http://test-areciboapp.appspot.com/
* Account number: "w3;5qwy45qshtqu46tdtgheq47s.ert6ew45e4i2w65"

Sending a HTTP POST in Python is easy using the urllib module. The most minimal request that can be sent just contains the API key, so let's send that as a first example::

    Python 2.4.4 (#1, Feb 18 2007, 22:11:27) 
    [GCC 4.0.1 (Apple Computer, Inc. build 5250)] on darwin
    Type "help", "copyright", "credits" or "license" for more information.
    >>> import urllib
    >>> data = {"account":"w3;5qwy45qshtqu46tdtgheq47s.ert6ew45e4i2w65"}
    >>> encoded = urllib.urlencode(data)
    >>> urllib.urlopen("http://test-areciboapp.appspot.com/v/1/", encoded).read()
    'Error recorded'

If the request is successful, a HTTP status of 200 will be returned.

The only thing you can really do wrong with this is get the API key wrong, Arecibo will do its best to record the error no matter what the error. If you've got some things in the POST that are wrong besides the API key, then Arecibo will simply log them on error. Sending a false API key will give you::

    >>> data = {"account":"wrongaccountnumber"}
    >>> encoded = urllib.urlencode(data)
    >>> urllib.urlopen("http://test-areciboapp.appspot.com/v/1/", encoded).read()
    'Problem recording the error: Account wrongaccountnumber does not exist.'

The request will also return a HTTP status of 500.

Once you've established how to make your error post, you can proceed to add in more variables. Here we are sending an error including the priority, status and some extra information in the msg::

    >>> data = {"account":"w3;5qwy45qshtqu46tdtgheq47s.ert6ew45e4i2w65", "status": 403, "priority": 1,
    ... "msg": "Someone tried to access /secure without the appropriate authorization"}
    >>> encoded = urllib.urlencode(data)
    >>> urllib.urlopen("http://test-areciboapp.appspot.com/v/1/", encoded).read()
    'Error recorded'

For more detailed and full examples on how to do a such a POST, please see the existing sample clients Python, Ruby or JavaScript libraries. For example the Python library does: UTF-8 encoding, checks for required variables and sets time outs to prevent leaving sockets open.

Notes for Authors
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* Where possible, set a timeout for your application posting to Arecibo, should Arecibo not be available, you do not want this to affect your site.

* Make sure your client library is robust, so that an error posting to Arecibo - either on your end formatting the data or on Arecibo's end - does not cause more errors. In the example Plone integrations when it cannot write to Arecibo because of some error, it logs to the local log file as a place of last resort.

* The more information you can pass the better.

* Sending every may not be useful we've found some errors that get continually reported may not be useful. So for example we ignore a 404 that might occur on: favicon.ico or robots.txt in the example integrations. If there are errors that just going to occur regularly, either don't send them or set them as very low priority.