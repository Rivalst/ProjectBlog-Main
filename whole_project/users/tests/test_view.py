from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


class UserLoginViewTest(TestCase):

    def setUp(self) -> None:
        self.url = reverse('login')
        self.user = User.objects.create_user(username='Bob', password='password')

    def test_login_success(self):
        response = self.client.post(self.url, {'username': 'Bob', 'password': 'password'})
        self.assertRedirects(response, reverse('home'))

    def test_login_fail(self):
        response = self.client.post(self.url, {'username': 'Bob', 'password': 'wrong_password'})
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, 'Invalid login or password')


class UserRegisterViewTest(TestCase):

    def setUp(self) -> None:
        self.url = reverse('register')
        self.valid_data = {
            'username': 'Bob',
            'email': 'test@mail.com',
            'password1': 'password123',
            'password2': 'password123'
        }

    def test_register_view(self):
        response = self.client.post(self.url, data=self.valid_data)
        self.assertEquals(response.status_code, 200)
