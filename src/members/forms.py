""" Forms """
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

class RegisterUserForm(UserCreationForm):
    """ Adding user registration form fields """
    email = forms.EmailField()
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)

    class Meta:
        """ Form fields """
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
