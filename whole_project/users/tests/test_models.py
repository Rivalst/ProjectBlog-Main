from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from users.models import Profile

User = get_user_model()


class UserProfileModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(username='Bob', password='password')

    def test_profile_create(self):
        Profile.objects.create(user=self.user)
        profile = Profile.objects.get(user=self.user)
        self.assertEquals(profile.user.username, 'Bob')
        self.assertEquals(profile.avatar, 'avatar.jpg')

