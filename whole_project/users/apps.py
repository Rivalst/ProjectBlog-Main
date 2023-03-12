from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'

    # settings for profile users that 'Profile' in models create when users register...
    def ready(self):
        import users.signals
