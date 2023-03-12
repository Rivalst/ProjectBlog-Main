from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User


class UsersLoginViewTest(TestCase):
    def setUp(self):
        self.url = reverse('login')
        self.user = User.objects.create_user(username='testuser', password='password')

    def test_login_with_valid_credentials(self):
        response = self.client.post(self.url, {'username': 'testuser', 'password': 'password'})
        self.assertRedirects(response, reverse('home'))

    def test_login_with_invalid_credentials(self):
        response = self.client.post(self.url, {'username': 'testuser', 'password': 'wrong_password'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Invalid login or password')
