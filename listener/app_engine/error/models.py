from django.db import models
from django.contrib import admin
from django.core.urlresolvers import reverse

from google.appengine.ext import db

from appengine_django.models import BaseModel

import urlparse               
import md5

class Error(BaseModel):
    # time error was received by this server
    timestamp = db.DateTimeProperty()

    ip = db.StringProperty()
    user_agent = db.StringProperty()
    user_agent_short = db.StringProperty()
    user_agent_parsed = db.BooleanProperty(default=False)
    operating_system = db.StringProperty()

    priority = db.IntegerProperty()
    status = db.StringProperty()
    
    raw = db.LinkProperty()
    domain = db.StringProperty()
    server = db.StringProperty()    
    query = db.StringProperty() 
    protocol = db.StringProperty()
    
    uid = db.StringProperty()
    type = db.StringProperty()    
    msg = db.TextProperty()
    traceback = db.TextProperty()
    
    errors = db.TextProperty()
    
    # time error was recorded on the client server
    error_timestamp = db.DateTimeProperty()
    request = db.TextProperty()
    username = db.StringProperty()
    fingerprint = db.StringProperty()
    
    read = db.BooleanProperty(default=False)

    class Meta:
        app_label = "listener"

    def _short(self, field, length):
        value = getattr(self, field)
        if len(value) > length:
            return "%s.." % value[length-2]
        return value
        
    def url_short(self): return self._short("url", 20)
    def type_short(self): return self._short("type", 20)
    def query_short(self): return self._short("query", 20)
    
    def get_absolute_url(self):
        return reverse("error-view", args=[self.id,])
    
    @property
    def id(self):
        return str(self.key())
            
    @property
    def title(self):
        """ Try to give a nice title to describe the error """
        strng = ""
        if self.type:
            strng = self.type
            if self.server:
                if self.status:
                    strng = "%s" % (strng)
                if not strng:
                    strng = "Error"
                strng = "%s on %s" % (strng, self.server) 
        elif self.status:
            strng = self.status
            if self.server:
                strng = "%s on server %s" % (strng, self.server)
        elif self.raw:
            strng = self.raw
        else:
            strng = self.nice_date()
        if self.uid:
            strng = "%s" % (strng)
        return strng

    @property
    def description(self):
        return self.msg or ""
    
    def calculate_fingerprint(self):
        """ Given an error, see if we can fingerprint it and find similar ones """
        keys = ["type", "traceback"]
        hsh = md5.new()
        
        found = False                           
        for key in keys:  
            value = getattr(self, key)
            if value:
                hsh.update(value.encode("ascii", "ignore"))
                found = True
        
        if found:
            self.fingerprint = hsh.hexdigest()
            self.save()
    
    def similar_fingerprint(self):
        """ Find all errors with a similar fingerprint """
        if self.fingerprint:
            results = Error.objects.filter(
                fingerprint=self.fingerprint).\
                exclude(id=self.id).\
                order_by("-error_timestamp", "-timestamp")
            return results
        else:
            return []