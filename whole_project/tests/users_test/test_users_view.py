import pytest
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.core import mail
from django.urls import reverse, reverse_lazy


from users.forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from users.models import Profile
from tests.blog_test.test_blog_view import create_context

User = get_user_model()


@pytest.fixture
def user_create():
    user = User.objects.create_user(username='Bob', password='password', email='test@mail.com')
    Profile.objects.get_or_create(user=user)
    return user


@pytest.fixture
def user_login_in(client, user_create):
    client.login(username=user_create.username, password='password')
    return user_create


class TestUserLoginView:

    @pytest.mark.django_db
    def test_user_login_successful(self, client, user_create):
        response = client.get(reverse('login'))
        assert response.status_code == 200

        response = client.post(reverse('login'), {'username': 'Bob', 'password': 'password'})
        assert response.status_code == 302
        assert response.url == reverse_lazy('home')

    @pytest.mark.django_db
    def test_user_login_fail(self, client):
        response = client.post(reverse('login'), {'username': 'Bob', 'password': 'incorrect'})
        mess = messages.get_messages(response.wsgi_request)
        assert response.status_code == 200
        assert 'Invalid login or password' in [m.message for m in mess]


class TestUserRegisterView:

    @pytest.mark.django_db
    def test_user_register_successful(self, client):
        valid_data = {'username': 'Bob2',
                      'email': 'test@mail.com',
                      'password1': 'Password12345Password',
                      'password2': 'Password12345Password'
                      }

        response = client.get(reverse('register'))
        assert response.status_code == 200
        assert 'form' in response.context and isinstance(response.context['form'], UserRegisterForm)

        response = client.post(reverse('register'), data=valid_data)
        assert response.status_code == 302
        assert response.url == reverse_lazy('home')

        assert User.objects.filter(username=valid_data['username']).exists()
        assert Profile.objects.filter(user__username=valid_data['username']).exists()
        assert response.client.session['_auth_user_id'] == str(User.objects.get(username=valid_data['username']).id)

    @pytest.mark.django_db
    def test_user_register_fail(self, client):
        invalid_data = {'username': 'Bob2',
                        'email': 'test@mail.com',
                        'password1': '',
                        'password2': ''
                        }

        response = client.post(reverse('register'), data=invalid_data)
        assert response.status_code == 200
        assert response.context['form'].errors


class TestUserLogoutView:

    @pytest.mark.django_db
    def test_user_logout(self, client, user_create, user_login_in):
        assert user_login_in.is_authenticated

        response = client.post(reverse('logout'))
        assert response.status_code == 302
        assert response.context is None


class TestUsersProfileSettingsView:

    @pytest.mark.django_db
    def test_get_user_profile_settings(self, client, user_create, user_login_in):
        response = client.get(reverse('profile-settings'))
        context = response.context

        assert response.status_code == 200
        assert context['user'] == user_login_in
        assert 'user_form' in context and isinstance(context['user_form'], UserUpdateForm)
        assert 'profile_form' in context and isinstance(context['profile_form'], ProfileUpdateForm)

    @pytest.mark.django_db
    def test_post_user_profile_settings(self, client, user_create, user_login_in):
        valid_data = {
            'username': 'John',
            'email': 'test2@mail2.com'
        }
        user_id = User.objects.get(username=user_create.username).id

        response = client.post(reverse('profile-settings'), data=valid_data, follow=True)
        assert response.status_code == 200
        assert response.context['user'] == User.objects.get(username=valid_data['username'])
        assert User.objects.get(username=valid_data['username']).email == valid_data['email']
        assert User.objects.get(username=valid_data['username']).id == user_id
        assert User.objects.get(username=valid_data['username']).profile.email_verified is False

        mess = messages.get_messages(response.wsgi_request)
        assert 'Your profile has been updated' in [m.message for m in mess]


class TestVerificationEmailView:

    @pytest.mark.django_db
    def test_send_verification_email(self, client, user_login_in):
        response = client.get(reverse('send_verification'))

        assert response.status_code == 302
        assert response.url == reverse_lazy('confirm_wait')

        email = mail.outbox[0]
        assert len(mail.outbox) == 1
        assert email.subject == 'Please verify your email'
        assert email.to == [user_login_in.email]


class TestAuthorDetailView:

    @pytest.mark.django_db
    def test_author_detail(self, client, create_context):
        user = create_context['user']
        response = client.get(reverse('author-view', kwargs={'pk': user.pk}))

        assert response.status_code == 200
        assert 'blogs' in response.context and len(response.context['blogs']) > 0
        assert 'blogs_last' in response.context and len(response.context['blogs_last']) <= 3
        assert 'tags' in response.context and len(response.context['tags']) > 0
        assert 'category' in response.context and len(response.context['category']) == 1

