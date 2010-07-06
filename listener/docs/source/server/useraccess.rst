User Access
=============================
Any user with a Google account can login to your Arecibo account, however they cannot view anything  at all until you give them access.

The first time
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

For the first time you log in to your site, you won't be able to access because you have not been given access. Administering users
to give them access requires admin rights, something you don't have yet. To gain admin rights, you log in through the Google App Engine
console and provide admin rights to the user you are going to be using.

To do this:

* Go to your App Engine admin console http://code.google.com/appengine/docs/theadminconsole.html

* Login, if needed as the Google user who has access to administer the site.

* Go to *your app* > *datastore viewer* > *user*

* Find the user you'd like to give access to, click on them

* Set "is_staff" to True

Every other time
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Once you've used the admin console, you can give any other user rights to administer the site using the admin console.

* In Arecibo go to *Users*, this will give you a list of users.

* Click on a user to toggle their access.

If by doing this you accidentally lock yourself out, or want to delete users from showing up there at all, you can use the App Engine admin
console as noted above to approve yourself or delete users.

Notes
~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you got Google Apps already for your domain, then you can restrict the login just to your domain in the App Engine console.
