from datetime import datetime

from app.base import Base
from appengine_django.models import BaseModel
from google.appengine.ext import db

from django.utils.translation import ugettext as _

stage_choices = (
    ["dev", _("Development")],
    ["testing", _("Testing")],
    ["staging", _("Staging")],
    ["backup", _("Backups")],
    ["production", _("Production")],
    ["other", _("Other")]
)

class Project(Base):
    name = db.StringProperty(required=True)
    description = db.TextProperty(required=False)

    def __str__(self):
        return self.name

class ProjectURL(Base):
    project = db.ReferenceProperty(Project)
    url = db.StringProperty(required=False)
    stage = db.StringProperty(required=False)

    def get_stage_display(self):
        return dict(stage_choices).get(self.stage)

    def __str__(self):
        return self.url
