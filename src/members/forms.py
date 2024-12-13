""" Forms """
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
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

class LoginUserForm(forms.Form):
    """Login form with validation for username and password"""
    username = forms.CharField(
        max_length=150,
        required=True,
    )
    password = forms.CharField(
        max_length=128,
        required=True,
    )

    class Meta:
        """ Form fields """
        model = User
        fields = ('username', 'password')

    def clean(self):
        """Validate username and password"""
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if not User.objects.filter(username=username).exists():
            raise forms.ValidationError({'username': 'The username does not exist.'})

        user = authenticate(username=username, password=password)
        if user is None:
            raise forms.ValidationError({'password': 'Incorrect password. Please try again.'})

        return cleaned_data
