import django
version = django.VERSION

if version[0] < 1 or version[1] < 2:
    raise ValueError("You need at least Django 1.2 to run Arecibo, "\
    "please see http://www.areciboapp.com/docs/server/installation.html.")