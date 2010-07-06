Example scripts
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

These are some example scripts to work with Arecibo differently.

Giving all users access automatically
---------------------------------------------------------

In *custom/listeners.py*, add the following:

.. code-block:: python

    from appengine_django.auth.signals import user_created

    def make_staff(sender, instance, **kw):
        if not instance.is_staff:
            instance.is_staff = True
            instance.save()

    user_created.connect(make_staff, dispatch_uid="make_staff")
