from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth import get_user_model


User = get_user_model()


class UserSignUpForm(UserCreationForm):
    email = forms.EmailField(required=True, label='E-mail')

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', )