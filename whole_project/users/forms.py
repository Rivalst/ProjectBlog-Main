from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from .models import Profile

User = get_user_model()

# ----- Form for register -----
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(max_length=254)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


# ----- End form for register -----

# ----- Form for update user profile -----

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar', ]


# ----- End form for update user profile -----

# ----- Form for user delete account -----

class DeleteAccountForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput)

# ----- End form for user delete account
