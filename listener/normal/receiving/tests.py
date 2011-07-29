from receiving import post
from django.conf import settings
from django.test import TestCase
from error.models import Error

class PostTest(TestCase):

    def test_post_key(self):
        settings.ANONYMOUS_POSTING = False
        acc = settings.ARECIBO_PUBLIC_ACCOUNT_NUMBER
        post.populate({'account': acc})
        assert(Error.objects.count() == 1)
        self.assertRaises(ValueError, post.populate, {'account': acc + "a"})

    def test_post_no_key(self):
        settings.ANONYMOUS_POSTING = True
        acc = settings.ARECIBO_PUBLIC_ACCOUNT_NUMBER
        post.populate({'account': acc})
        assert(Error.objects.count() == 1)
        post.populate({})
        assert(Error.objects.count() == 2)
        settings.ANONYMOUS_POSTING = False
