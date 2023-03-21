from django.urls import path
from . import views

from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView, PasswordResetCompleteView, \
    PasswordResetDoneView
from django.views import generic

urlpatterns = [
    # ----- main path -----
    path('login/', views.UsersLoginView.as_view(), name='login'),
    path('register/', views.UsersRegisterView.as_view(), name='register'),
    path('logout/', views.UsersLogoutView.as_view(), name='logout'),
    path('profile-settings/', views.UsersProfileSettingsView.as_view(), name='profile-settings'),
    path('profile/', views.UserProfileView.as_view(), name='profile'),
    # ----- end main path -----

    # ----- delete account -----
    path('profile-settings/delete-account/', views.UsersDeleteAccountView.as_view(), name='delete-account'),
    path('verify_delete_account/<uidb64>/<token>', views.UsersDeleteAccountVerifyView.as_view(),
         name='verify_delete_account'),
    # ----- end delete account -----

    # ----- verify email -----
    path('send_verification_email/', views.SendVerificationEmailView.as_view(), name='send_verification'),
    path('verify_email/<uidb64>/<token>', views.VerifyEmailView.as_view(), name='verify_email'),
    path('confirm_wait/', generic.TemplateView.as_view(template_name='users/confirm_wait.html'), name='confirm_wait'),
    # ----- end verify email -----

    # ----- change password -----
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
    # ----- end change password -----
]
