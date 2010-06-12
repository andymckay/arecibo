Sample Ruby Client
====================================

The Ruby client allows you to easily send errors via HTTP. The Ruby client can be used independently, or as part of a greater implementation. Quick example:

.. code-block:: ruby

    require 'arecibo'
    dict = {
        :account => 'yourpublicaccountnumber',
        :priority => 1,
        :url => "http://badapp.org",
        :uid => "123124123123",
        :ip => "127.0.0.1",
        :type => "An error",
        :server => "Test Script"
    }
    p = Arecibo.new("http://yoursite/v/1/", dict)
    p.send

Requirements
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* If using the http client, permission to make a HTTP post to the Arecibo server is needed.

Notes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* No values are automatically set.

* There is 10 second timeout set on the HTTP post to prevent hangs.