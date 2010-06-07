User Access
=============================
Any user with a Google account can login to your Arecibo account, however they cannot view anything  at all until you give them access.

* Go to your App Engine admin console http://code.google.com/appengine/docs/theadminconsole.html

* Login, if needed as the Google user who has access to administer the site.

* Go to *your app* > *datastore viewer* > *user* 

* Find the user you'd like to give access to, click on them

* Set "is_staff" to True

If you got Google Apps already for your domain, then you can restrict the login just to your domain in App Engine.
