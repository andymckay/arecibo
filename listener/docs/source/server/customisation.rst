Customising the server
=============================

The server is not designed to be completely customisable, but rather to have some key customisation points you can alter. The main target for customisation is in the workflow - that is when and how errors are processed. Rather than give a lot of large forms full of options, we'd rather focus on some scripts to allow this to happen.

The default area for customisation is within the custom folder. Being open source, you can of course change as much as you wish, however you then have more patches to maintain as Arecibo progresses.

Signals
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Arecibo uses Django's signal handling mechanism to deal with customizing. Whenever an item is created, signals are sent and those can be caught, default behaviour changed and so on as required. The signals are:

* *user_created*: sent when a user is created

* *error_created*: sent when an error is created

* *group_created*: sent when an error grouping is created

* *group_assigned*: sent when a group is created

* *error_assigned*: sent when an error is assigned to group

* *notification_created*: sent when a notification is created

You can connect your own methods to these signals, or disconnect the default methods, as you would like. By default the Python script at *custom/listeners.py* is imported, so this a good place to do this customisation.

Default methods
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The following are the default methods that are run on the signals. Feel free to turn these off or replace with whatever method you'd like.

default_grouping
+++++++++++++++++++++++++++++++++

**Connected to**: error_created
**Location**: from error.listeners import default_grouping

This is how errors are grouped together. By default it does it by adding together the fields: type, server, msg and status. If you'd like to remove this, then add the following to *custom/listeners.py*::

    from error.signals import error_created
    from error.listeners import default_grouping

    error_created.disconnect(default_grouping, dispatch_uid="default_grouping")

If you'd like to create your own group system you can do this by attaching a new signal::

    from error.signals import error_created

    def my_grouping(instance, **kw):
        pass # your code here

    error_created.connect(my_grouping, dispatch_uid="my_grouping")

default_browser_parsing
+++++++++++++++++++++++++++++++++

**Connected to**: error_created
**Location**: from error.listeners import default_browser_parsing

This parses the user agent string sent by the error into something more recognizable, producing the browser and operating system. However if you'd like something a little more custom you can do that. If you'd like to remove this, then add the following to *custom/listeners.py*::

default_notification
+++++++++++++++++++++++++++++++++

**Connected to**: error_created
**Location**: from notifications.listeners import default_notification

This parses the error and figures out if a notification needs to be sent. This is a good opportunity to customize what notification is sent to whom. The actual email (or whatever) will be
sent by a cron job, this process is just to figure out the list of notifications that are to be sent.

default_project
++++++++++++++++++++++++++++++++++

**Connected to**: group_assigned
**Location**: from projects.listeners import default_project

This figures out what project the group gets attached to.

Customising templates
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you would like to customise a template, then place it in custom templates. The easiest way to do this is to find
the template you'd like to customise, copy it into that folder and then make your changes.
