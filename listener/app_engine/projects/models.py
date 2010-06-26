from datetime import datetime

from appengine_django.models import BaseModel
from google.appengine.ext import db

stage_choices = (
    ["dev", "Development"],
    ["testing", "Testing"],
    ["staging", "Staging"],
    ["backup", "Backups"],
    ["production", "Production"],
    ["other", "Other"]    
)

class Project(BaseModel):
    name = db.StringProperty(required=True)
    description = db.TextProperty(required=False)
    
    @property
    def id(self):
        return str(self.key())

class ProjectURL(BaseModel):
    project = db.ReferenceProperty(Project)
    url = db.StringProperty(required=False)
    stage = db.StringProperty(required=False)
    
    @property
    def id(self):
        return str(self.key())
        
    def get_stage_display(self):
        return dict(stage_choices).get(self.stage)
    