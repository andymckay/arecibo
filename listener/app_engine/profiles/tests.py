from django.test import TestCase

from appengine_django.auth.models import User as AppUser
from google.appengine.api.users import User

from profiles.models import Profile
from profiles.utils import get_profile

class TestProfile(TestCase):
    
    def setUp(self):
        for user in AppUser.all(): user.delete()
        for profile in Profile.all(): profile.delete()

    def test_add_user(self):
        user = AppUser(user=User(email="test@foo.com"),
                       username="test",
                       email="test@foo.com",
                       is_staff=True).save()
        assert not Profile.all().count()
        profile = get_profile(user)
        assert profile.notification == 5
        assert Profile.all().count()
