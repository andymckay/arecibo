Sample Python Client
====================================

The Python client allows you to easily send errors either via HTTP. The Python client can be used independently, or as part of a greater implementation. Quick example::

    from arecibo import post
    arecibo = post()
    arecibo.set("account", "yourpublicaccountnumber")
    arecibo.set("status", "403")
    arecibo.set("url", "http://badapp.org")
    arecibo.send()

Requirements
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Tested on Python 2.4 and 2.5, however any 2.x version of Python is likely to be sufficient. Permission to make a HTTP post to the Arecibo server is needed. 

Notes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* The only value set automatically is server, which we set to the output of socket.gethostname() (if that's available)

* To prevent timeouts, the library does change the socket timeout value, sends the HTTP request and then instantly sets it back to the original value. This should minimize the impact on any other socket connections.