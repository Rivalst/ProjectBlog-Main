from django.urls import path
from . import views

from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView, PasswordResetCompleteView, \
    PasswordResetDoneView

urlpatterns = [
    path('login/', views.UsersLoginView.as_view(), name='login'),
    path('register/', views.UsersRegisterView.as_view(), name='register'),
    path('logout/', views.UsersLogoutView.as_view(), name='logout'),
    path('profile-settings/', views.UsersProfileSettingsView.as_view(), name='profile-settings'),

    path('password-reset/', PasswordResetView.as_view(template_name='users/password_reset.html'),
         name='password-reset'),

    path('password-reset-done/', PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'),
         name='password_reset_done'),

    path('password-reset-confirm/<uidb64>/<token>/',
         PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'),
         name='password_reset_confirm'),

    path('password-reset-complete/',
         PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'),
         name='password_reset_complete'),
]
