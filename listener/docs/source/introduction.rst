Introduction to Arecibo
==============================

Arecibo is an error tracker. It allows you to log errors from web sites and collect them all in one location. It then allows you to prioritise and group them. Notifications can then be sent to developers of the errors.

There are two main components to Arecibo:

* client, this is normally a web application on residing on a server that sends an error into Arecibo. If there isn't an existing API for your application, then there's an API you can use to build your own.

* server, this is your instance of Arecibo that you can use to receive errors.

The server was written to run on App Engine in 2010. In 2011 a none App Engine port was made that should run in a "standard" environment. The App Engine port is essentially frozen now with no new updates. It works, but isn't realy developed. This situation may change, but if we can recommend a version to use, don't use the App Engine one.

There is also a bit of feature fork between the two. Primarily the App Engine one has an Issue tracker. The none App Engine one does not. Because of it's use at Mozilla the none App Engine one has no need of an Issue tracker.

The best way to get a feel for what Arecibo does, is to give the demo server a try. The details of the demo server are at http://www.areciboapp.com/demo
