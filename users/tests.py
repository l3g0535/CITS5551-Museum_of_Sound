from django.test import TestCase

# Create your tests here.
from mixer.backend.django import mixer
from user.models import Profile

class TestModels:

    def test_Profile_storagelocation(models.Model):
        Profile = mixer.blend('users.Profile', storage_location ='Profile')
        assert Profile.storage_location == 'Profile'

    def test_Profile_ID(models.Model):
        Profile = mixer.blend('users.Profile', user = '123')
        assert Profile.user == '123'

    def test_Profile_Title(models.Model):
        Profile = mixer.blend('users.Profile', image = 'test1')
        assert Profile.image == 'test1'
