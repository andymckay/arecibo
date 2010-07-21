# License: GPL
# Author: Andy McKay, Clearwind
#
# you will need growl for this, the binary and the source
# http://growl.info/source.php
# and then in Growl-1.2-src/Bindings/python run setup.py
# then this should work...
import Growl
import urllib

# requires 2.6
import json
import time
import os
from datetime import datetime

# the URL to your arecibo instance... remember you can use the query string to filter
url = "http://test-areciboapp.appspot.com/feed/sw3tqw35ywq45ws4kqa4ia6yw5q45serws23w351245lk6y/json/"
delay = 30

filename = os.path.expanduser("~/.arecibo-last")

class notifier(object):
    def __init__(self):
        self.gn = Growl.GrowlNotifier("arecibo", ["status",])
        self.gn.register()
        image_path = os.path.join(os.path.dirname(__file__), "apple-touch-icon.png")
        self.image = Growl.Image.imageFromPath(image_path)

    def load(self):
        if os.path.exists(filename):
            try:
                return self.convert(open(filename).read())
            except ValueError:
                pass
        return datetime.min

    def convert(self, string):
        return datetime.strptime(string, "%Y-%m-%d %H:%M:%S")

    def save(self, last_date):
        filehandle = open(filename, "w")
        filehandle.write(last_date.strftime("%Y-%m-%d %H:%M:%S"))
        filehandle.close()

    def get(self):
        unparsed = urllib.urlopen(url).read()
        parsed = json.loads(unparsed)
        highest = last_date = self.load()
        for error in parsed:
            dt = self.convert(error["fields"]["error_timestamp"][:19])
            if dt > last_date:
                self.gn.notify("status", "Arecibo error (priority %s)" % error["fields"]["priority"], "%s at %s\n%s" % (
                    error["fields"]["status"],
                    error["fields"]["domain"],
                    dt.strftime("%d %B, %H:%M")),
                    icon=self.image,
                    sticky=error["fields"]["priority"]==1)
            highest = max(highest, dt)
        self.save(highest)

if __name__=="__main__":
    anotifier = notifier()
    while True:
        anotifier.get()
        time.sleep(delay)
