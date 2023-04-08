from django.contrib import admin

from .models import Profile, Subscribers

admin.site.register(Profile)  # register Profile model in admin page
admin.site.register(Subscribers)
