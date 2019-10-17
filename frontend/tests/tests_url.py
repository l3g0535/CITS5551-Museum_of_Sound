from django.test import TestCase
from frontend.models import *
from django.test import Client

class URLTest(TestCase):
    def test_get_urls(self):
        c = Client()
        get_urls = ['','/production','/signup','/production/upload','/sound/record','/sound/upload',
        '/privacy','/aboutus','/licensing']
        for url in get_urls:
            response = c.get(url)
            self.assertTrue(response.status_code in [200, 302])

    def test_post_urls(self):
        pass
