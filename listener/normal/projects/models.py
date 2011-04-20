from datetime import datetime

from django.db import models

from django.utils.translation import ugettext as _

stage_choices = (
    ["dev", _("Development")],
    ["testing", _("Testing")],
    ["staging", _("Staging")],
    ["backup", _("Backups")],
    ["production", _("Production")],
    ["other", _("Other")]
)

class Project(models.Model):
    name = models.CharField(blank=False, max_length=255)
    description = models.CharField(blank=False, max_length=255)

    def __unicode__(self):
        return self.name

class ProjectURL(models.Model):
    project = models.ForeignKey(Project)
    url = models.CharField(blank=False, max_length=255)
    stage = models.CharField(choices=stage_choices, blank=False, max_length=255)

    def get_stage_display(self):
        return dict(stage_choices).get(self.stage)

    def __unicode__(self):
        return self.url
