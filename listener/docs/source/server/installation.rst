Installation (Linux)
====================================

Requirements
----------------------------

The installation has been tested on Ubuntu Linux. It should work on any Linux installation, it might even work on Windows.

You will require:

- Connection to a database either locally or remotely. We recommend Postgresql [1]_.

- Access to a Celery queue and a corresponding backend [2]_.

- A working Django 1.3 will be installed, or use an existing one [3]_. Packages are installed via pip [4]_.

- A working Python 2.4 or greater installation [5]_. 

- You will need git to check out Arecibo from github [6]_.

- You will need a web server, this documentation covers Apache [7]_ and mod_wsgi [8]_, but others will work.


Installation steps
------------------------------------------------

The following steps are done on Ubuntu Linux. Other operating systems may vary.

1. Download Arecibo
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Create a directory to install Arecibo too. Run the following command::

    ~ $ git clone git://github.com/andymckay/arecibo.git
    Cloning into arecibo...
    ... done.   

2. Install dependencies
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You must have at least Python 2.4 as noted above and pip so that you can install the Python dependencies. Virtual environment setup is recommended, but not required. Run the following::

    ~ $ pip install -r arecibo/listener/normal/requirements.txt
    Downloading/unpacking Django==1.3
    ... 

The other dependencies: database, web server, celery backend (eg Rabbit MQ) should be installed now.

3. Configure Arecibo
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Run::

    ~ $ cd arecibo/listener/normal
    ~/arecibo/listener/normal $ cp local_settings.py.dist local_settings.py

Then configure local_settings.py with at least:

* the Django database configuration

* the Django secret key

* any other Django configuration that needs overriding, such as celery.

Run::

    ~/arecibo/listener/normal $ python manage.py syncdb

Create your super user. You should now be able to run::

    ~/arecibo/listener/normal $ python manage.py runserver
    
And see it all working.

4. Configure Apache
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Run::

    ~/arecibo/listener/normal $ cd config
    ~/arecibo/listener/normal/config $ cp arecibo.wsgi.sample arecibo.wsgi
    
Now link that up in Apache::

    WSGIScriptAlias / /path/to/arecibo/listener/normal/config/arecibo.wsgi

Further configuration options would include mapping *media* to the static media files inside Arecibo *listener/media*.

Restart Apache and you should be able to see Arecibo.

5. Final test
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Change *local_settings.py*::

    ANONYMOUS_POSTING = True
    
Then hit::

    http://path.to.arecibo/v/1/
    
And you should get a response: Error recorded.

Anything else means you need to check your database connection and that Django
can speak to the celery queue.

.. [1] http://www.postgresql.org/

.. [2] http://ask.github.com/celery/

.. [3] http://www.djangoproject.com/

.. [4] http://pypi.python.org/pypi/pip

.. [5] http://www.python.org/

.. [6] http://git-scm.com/

.. [7] http://httpd.apache.org/

.. [8] http://code.google.com/p/modwsgi/
