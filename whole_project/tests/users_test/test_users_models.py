import pytest

from users.models import Profile

from tests.users_test.test_users_view import user_login_in, user_create


class TestModelProfile:

    @pytest.mark.django_db
    def test_user_profile_create(self, client, user_login_in, user_create):
        prof_user = Profile.objects.get(user__username=user_login_in.username)
        assert prof_user is not None
        assert prof_user.avatar == 'avatar.jpg'
        assert prof_user.email_verified is False
