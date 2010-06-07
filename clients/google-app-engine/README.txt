This is the next version of the Arecibo API which connects to the Google App Engine implementation of Arecibo.

Arecibo is an open source application to provide error logging and notifications for your web sites.

See http://areciboapp.com/docs/client/django.html for more information

* Because when you upload an app to App Engine you can't specify other libraries to use, you pretty much have to include this module in your App Engine source.

* The main API is HTTP.

* Email is a bit problematic because Gmail inserts new lines into plain-text emails when you send them. These new lines break the JSON.

* This requires Django, but only because the standard settings are pulled in from django.conf, if you aren't using Django on App Engine, replace that with something else.