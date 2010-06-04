Variable documentation
====================================

This covers all the variables that can be sent in a post to Arecibo. There is only one required variable: your public API key. All others are optional, leaving it to you to figure out exactly how much you data you want to send to the server.

Required variables
------------------------------------

account
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The public API key for your account on Arecibo. Without it we don't know where to assign the request. This is the public API key as defined in the API key page.
::
    account = "123123124124..."

Optional variables
------------------------------------

All the following examples use the JavaScript API as examples. All values are taken to be strings.

status
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Limit:** length of 3 and a valid status code

The HTTP status code that is returned. This must be a valid status code [#f1]_; any other values are ignored.
::
    status = "404"

priority
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Limit:** empty or between 1 and 10

A number between 1 and 10. The values 1 to 3 are coloured in the web interface, with number 1 being the most important. A user can configure notifications to be sent to them when errors are above a certain priority.

::
    priority = "3"
    
    
A standard a 404 "Page not found" could be priority 5. They could occur regularly and there may not be much you can do about them. However, if a "Page not found" has a referer from your site, then you could assign priority of 3, since this is something you may be able to fix. A 500 "Server Error" could be priority 1.

ip
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Limit:** 15 chars

The IP address of the client triggering the error. If you are setting this on your server, be sure to take into account any proxies that might be in the way.

:: 
    ip = "192.168.1.53"

user_agent
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Limit:** 255 chars

The user agent string that the client sends will provide a great deal of information about the browser, operating system and so on. Please note, however, that this can be easily faked and cannot be relied on 100%.

::
    user_agent = "Mozilla/5.0 (Macintosh; U; Intel Mac OS X..."

url
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Limit:** 10,000 chars

The full URL making the request at that time. Include any GET parameters in your URL so that these are properly processed.

::
    url = "http://clearwind.ca/this/url/does/not/exist?test=yes"

uid
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Limit:** 255 chars

A unique id generated for each error. This uid can be included in an error message to the user. The user can then include this uid when inquiring about an error. A unique id for a simple site could be the output of a timestamp. However, on a large site this can cause confusion when there are concurrent errors; therefore a more complex uid may be necessary. Arecibo does not require this value to be unique, but if there are multiple errors with the same id, the administrator would have to sort out which was which.

::
    uid = "1256235123.1020"

Providing a uid to the user is helpful because you can simply tell the user to contact you with the uid and you can look it up.

type
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Limit:** 255 chars

The type of error that has occurred, for example a DatabaseError. This string is completely up to you.
type = "ZeroDivisionError"

server
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Limit:** 1,024 chars, UTF-8 encoding

The name of the server the error is occurring on. This allows you to identify the actual server, useful for when you have a web site balanced across several servers.

::
    server = "serverA"

msg
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Limit:** 10,000 chars, UTF-8 encoding

A message that goes along with this error. This could be a more detailed error returned by your application. It could also be your chance to include any other notes you feel relevant to this issue. All HTML is ignored on the server.

::
    msg = "Lorem ipsum dolor sit amet..."

traceback
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Limit:** 10,000 chars, UTF-8 encoding

If your application provides a useful stack trace, then here is the opportunity to include it, this is arguably one of the most important elements, so include it if you can. All HTML is ignored and there is a limit to the amount of text sent.

::
    traceback = "[COMException (0x80040154): Retrieving the COM class factory
       for component with CLSID {4D880EAB-BF35-423A-A859-B1D9F2AC4CC1} failed 
       due to the following error: 80040154.]"

timestamp
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Limit:** valid string

The time that the error occurs. The date and time that Arecibo needs is the current time for the GMT time zone. The format is as specified by RFC 2822, for example: Fri, 02 Jan 2009 19:19:51 -0000. As convenience, we also accept a prefix of GMT which is interpreted as -0000.

::
    var now = new Date;
    timestamp = now.toUTCString();

request
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Limit:** 10,000 chars, UTF-8 encoding

Text of all the request variables sent with the request. This is a text area where you can capture any other particular variables you thing might be relevant.

::
    request = "..."

username
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Limit:** 255 chars

If your application has a username, this is the user that is currently using the application. If you know specifically that it's an Anonymous user, setting this to "Anonymous" will it make clear that you know there was no user logged in.

::
    username = "Bob the Builder"

Notes
------------------------------------

* Text in the following fields: traceback, msg, type and server are assumed to be UTF-8 encoding. We plan on supporting other encoding later, but at the moment everything is tested with UTF-8 data. All other fields are ASCII strings.

* Any text over the limit for that field will be truncated. An error will be written into the error field (visible on a view) so you can spot this and correct.

* We won't reject any error, unless it has an invalid private key. The error will still be written so one mistake in the posting of data does not invalidate the whole report.

* All HTML is going to be quoted for display, so feel free to send any HTML without worrying about security.

.. rubric:: Footnotes

.. [#f1] Valid HTTP statuses are: 100, 101, 102, 200, 201, 202, 203, 204, 205, 206, 207, 226, 300, 301, 302, 303, 304, 305, 307, 400, 401, 402, 403, 404, 405, 406, 407, 408, 409, 410, 411, 412, 413, 414, 415, 416, 417, 422, 423, 424, 426, 500, 501, 502, 503, 504, 505, 507, 510.