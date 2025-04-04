from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from apps.users.models import User


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'name', "role", "image"]
        error_class = "error"


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['username', "name", "role", "image"]
        error_class = "error"


class NewPasswordForm(forms.Form):
    new_password = forms.CharField()
    re_new_password = forms.CharField()
