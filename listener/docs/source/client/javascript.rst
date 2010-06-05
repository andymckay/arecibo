Sample Javascript (Browser) Client
====================================

The JavaScript (Browser) client is probably the easiest of all the possible clients to set up and we recommend trying it first. It also provides the greatest flexibility in terms of being platform agnostic.

To install simply add the following to your *error* page::

    <script type="text/javascript" src="http://your-site-name.com/lib/error.js">
    </script>
    <script type="text/javascript">
      arecibo.account = 'yourpublicaccountnumber';
      arecibo.run();
    </script>

Notes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The following variables are automatically assigned: ip, user_agent, url. However any of them may be overridden, with your own values should you want to.

An object is created called arecibo. Variables would be assigned in the following manner::

    arecibo.variable = name

For example to set a status and priority, you would add in more values::

    <script type="text/javascript" src="http://your-site-name.com/lib/error.js">
    </script>
    <script type="text/javascript">
      arecibo.account = 'yourpublicaccountnumber';
      arecibo.status = 500;
      arecibo.priority = 1;
      arecibo.run();
    </script>

Advantages
~~~~~~~~~~~~~~~~~~~~~~~~~~

* Can be used on any website regardless of programming language or configuration.

* Requires minimal install, we include it by default with Arecibo.

Disadvantages
~~~~~~~~~~~~~~~~~~~~~~~~~~

* Requires client to have JavaScript enabled. Most browsers will have this enabled; however, robots and other programs will not. On the other hand, do you really want to get all 404's from robots?

* Exposes your public key to others who may also use this key.

* Exposes variables and data in the source. You may not want this information to be known for security purposes.