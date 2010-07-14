# Copyright 2008 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
App Engine compatible models for the Django authentication framework.
"""

from django.core import mail
from django.core.exceptions import ImproperlyConfigured
from django.db import models
from django.utils.encoding import smart_str
import urllib

from django.db.models.manager import EmptyManager

from google.appengine.api import users
from google.appengine.ext import db

from appengine_django.models import BaseModel
from appengine_django.auth.signals import user_created

class User(BaseModel):
  """A model with the same attributes and methods as a Django user model.

  The model has two additions. The first addition is a 'user' attribute which
  references a App Engine user. The second is the 'get_djangouser_for_user'
  classmethod that should be used to retrieve a DjangoUser instance from a App
  Engine user object.
  """
  user = db.UserProperty(required=True)
  username = db.StringProperty(required=True)
  first_name = db.StringProperty()
  last_name = db.StringProperty()
  email = db.EmailProperty()
  password = db.StringProperty()
  is_staff = db.BooleanProperty(default=False, required=True)
  is_active = db.BooleanProperty(default=True, required=True)
  is_superuser = db.BooleanProperty(default=False, required=True)
  last_login = db.DateTimeProperty(auto_now_add=True, required=True)
  date_joined = db.DateTimeProperty(auto_now_add=True, required=True)
  groups = EmptyManager()
  user_permissions = EmptyManager()

  def __unicode__(self):
    return self.username

  def __str__(self):
    return unicode(self).encode('utf-8')

  @classmethod
  def get_djangouser_for_user(cls, user):
    query = cls.all().filter("user =", user)
    if query.count() == 0:
      django_user = cls(user=user, email=user.email(), username=user.nickname())
      django_user.save()
    else:
      django_user = query.get()
    return django_user

  def set_password(self, raw_password):
    raise NotImplementedError

  def check_password(self, raw_password):
    raise NotImplementedError

  def set_unusable_password(self):
    raise NotImplementedError

  def has_usable_password(self):
    raise NotImplementedError

  def get_group_permissions(self):
    return self.user_permissions

  def get_all_permissions(self):
    return self.user_permissions

  def has_perm(self, perm):
    return False

  def has_perms(self, perm_list):
    return False

  def has_module_perms(self, module):
    return False

  def get_and_delete_messages(self):
    """Gets and deletes messages for this user"""
    msgs = []
    for msg in self.message_set:
      msgs.append(msg)
      msg.delete()
    return msgs

  def is_anonymous(self):
    """Always return False"""
    return False

  def is_authenticated(self):
    """Always return True"""
    return True

  def get_absolute_url(self):
    return "/users/%s/" % urllib.quote(smart_str(self.username))

  def get_full_name(self):
    full_name = u'%s %s' % (self.first_name, self.last_name)
    return full_name.strip()

  def email_user(self, subject, message, from_email):
    """Sends an email to this user.

    According to the App Engine email API the from_email must be the
    email address of a registered administrator for the application.
    """
    mail.send_mail(subject,
                   message,
                   from_email,
                   [self.email])


  @property
  def pk(self):
    try:
      return str(self.key())
    except db.NotSavedError:
      pass

  def get_profile(self):
    """
    Returns site-specific profile for this user. Raises
    SiteProfileNotAvailable if this site does not allow profiles.

    When using the App Engine authentication framework, users are created
    automatically.
    """
    from django.contrib.auth.models import SiteProfileNotAvailable
    if not hasattr(self, '_profile_cache'):
      from django.conf import settings
      if not hasattr(settings, "AUTH_PROFILE_MODULE"):
        raise SiteProfileNotAvailable
      try:
        app_label, model_name = settings.AUTH_PROFILE_MODULE.split('.')
        model = models.get_model(app_label, model_name)
        self._profile_cache = model.all().filter("user =", self).get()
        if not self._profile_cache:
          raise model.DoesNotExist
      except (ImportError, ImproperlyConfigured):
        raise SiteProfileNotAvailable
    return self._profile_cache

  def save(self):
      created = False
      if not hasattr(self, "id"):
        created = True
      super(User, self).save()
      if created:
        user_created.send(sender=self.__class__, instance=self)

class Group(BaseModel):
  """Group model not fully implemented yet."""
  # TODO: Implement this model, requires contenttypes
  name = db.StringProperty()
  permissions = EmptyManager()


class Message(BaseModel):
  """User message model"""
  user = db.ReferenceProperty(User)
  message = db.TextProperty()


class Permission(BaseModel):
  """Permission model not fully implemented yet."""
  # TODO: Implement this model, requires contenttypes
  name = db.StringProperty()
