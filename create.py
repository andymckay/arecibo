import re
import sys
import os
import random
import hashlib
import time
import string
import shutil
import urllib
import tarfile

def key(phrase, type):
    m = hashlib.md5()
    m.update(str(time.time()))
    m.update(phrase)
    m.update(type)
    m.update("".join(random.sample(string.lowercase, 3)))
    return m.hexdigest()

def create():
    print "Create new Arecibo instance."
    print "Enter location locally to create an instance: "
    directory = sys.stdin.readline().strip()
    if not directory:
        print "Error: directory required"
        sys.exit(1)
    
    print "Name of remote app engine instance: "
    name = sys.stdin.readline().strip()
    if not name:
        print "Error: app engine instance name required"
        sys.exit(1)
        
    print "Gmail account used to manage app engine instance: "
    email = sys.stdin.readline().strip()

    print "Key passphrase (type in a few chars): "
    phrase = sys.stdin.readline().strip()
    private = key(phrase, "private")
    public = key(phrase, "public")
    if os.path.exists(directory):
        print "Error: directory already exists."
        sys.exit(1)
    
    print
    print "Creating directory... %s" % directory
    parent = os.path.dirname(directory)
    if not os.path.exists(parent) and parent:
        os.makedirs(parent)
    src = os.path.join("listener", "app_engine")
    print "Copying over Arecibo... "
    shutil.copytree(src, directory)
    print "Creating app.yaml... "
    src = os.path.join(directory, "app.yaml.example")
    dest = src[:-8]
    shutil.copy(src, dest)
    data = open(dest, "rb").read()
    data = data.replace("application: your_application_error", "application: %s" % name)
    outfile = open(dest, "wb")
    outfile.write(data)
    outfile.close()
    print "... set application id."
    
    print "Creating local_settings.py... "
    src = os.path.join(directory, "local_settings.py.example")
    dest = src[:-8]
    shutil.copy(src, dest)
    data = open(dest, "rb").read()
    data = data.replace('your_public_account_number_here', public)
    data = data.replace('your_private_account_number_here', private)
    data = data.replace('theurl.to.your.arecibo.instance.com', '%s.appspot.com' % name)
    data = data.replace('you.account@gmail.com.that.is.authorized.for.app_engine', email)
    print "... set public, private keys."
    print "... set url and email."
    outfile = open(dest, "wb")
    outfile.write(data)
    outfile.close()

    django = "http://www.djangoproject.com/download/1.2.3/tarball/"
    print "Attempting to download django from:"
    print "... %s" % django
    try:
        filename, response = urllib.urlretrieve(django)
    except IOError:
        print "... download failed."
        print "Please download django and continue install as per:"
        print "http://areciboapp.com/docs/server/installation.html"
        return    
    
    print "Extracting django..."
    tar = tarfile.open(filename)
    tar.extractall(directory)
    tar.close()

    print "Copying over to Arecibo"
    shutil.copytree(os.path.join(directory, "Django-1.2.3", "django"), 
                    os.path.join(directory, "django"))
    shutil.rmtree(os.path.join(directory, "Django-1.2.3"))
    print "...complete."
    print "Arecibo local installation at: %s" % directory

if __name__=='__main__':
    create()
