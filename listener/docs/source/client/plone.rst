Sample Plone client
=======================================

This is a specific Arecibo implementation for Plone.

Installation
~~~~~~~~~~~~~~~~~~~~~~~~~~~
Add in the following into your *buildout.cfg*. Under eggs add::

    clearwind.arecibo

Under zcml add::

    clearwind.arecibo

Re-run buildout and restart Plone. Then

* Go to your Add/Remove Products and install Arecibo. 

* Then enter your Arecibo public API key.

Installation is now complete.

Requirements
~~~~~~~~~~~~~~~~~~~~~~~~~~~

* Tested on Plone 3.1.5.1, it uses eggs and would be unlikely to work on anything earlier than this. However the core part of the code to send to Arecibo could be easily refactored into Plone 3 or 2 if needed.

* If you wish to use the HTTP transport, then the Plone process will need to be allowed to make HTTP posts to the Arecibo server.

Notes
~~~~~~~~~~~~~~~~~~~~~~~~~~~

* By default we set all 404 as priority 5, 500 as priority 1 and the rest as priority 3. This can be altered in the wrapper.py module.

* The UID that Plone generates is passed on to Arecibo, meaning that by default: UID (for 500 errors only), IP, server, type, traceback, status, user_agent, url, server, priority and notes are set.

* To prevent timeouts, the library does change the socket timeout value, sends the HTTP request and then sets it back to the original value. This should minimize the impact on any other socket connections.

* Redirect errors are ignored.