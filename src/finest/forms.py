""" Form creation and validation """
from urllib.parse import urlparse
import os
from django import forms
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .models import Contact, SubmittedWebsite, Review, Profile

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

class SubmittedWebsiteForm(forms.ModelForm):
    """ Form validation """
    class Meta:
        """ SubmittedWebsiteForm fields """
        model = SubmittedWebsite
        fields = ['title', 'url', 'description', 'file']

    title = forms.CharField(required=True, max_length=255)
    url = forms.URLField(required=True)
    description = forms.CharField(required=True)
    file = forms.FileField(required=True)

    def clean_title(self):
        """ title validation """
        title = self.cleaned_data.get('title')
        if len(title) > 255:
            raise forms.ValidationError("The title should not exceed 255 characters.")
        return title

    def clean_url(self):
        """ URL validation """
        url = self.cleaned_data.get('url')

        if not url.startswith(('http://', 'https://')):
            raise ValidationError("The URL must start with 'http://' or 'https://'")

        parsed_url = urlparse(url)
        if not parsed_url.netloc:
            raise ValidationError("The URL must be a valid URL.")

        return url

    def clean_file(self):
        """ File validation """
        file = self.cleaned_data.get('file')
        max_size_kb = 5000
        allowed_extensions = ['.jpg', '.jpeg', '.png', '.webp']
        ext = os.path.splitext(file.name)[1].lower()

        if file.size > max_size_kb * 1024:
            raise forms.ValidationError("File size cannot exceed 5 MB.")
        if ext not in allowed_extensions:
            raise forms.ValidationError("Only .jpg, .jpeg, .png, .webp files are allowed.")
        return file


class ReviewForm(forms.ModelForm):
    """ Review Form """
    class Meta:
        """ Class Meta"""
        model = Review
        fields = ['design', 'usability', 
                  'content', 'overall', 'description']
        widgets = {
            'design': forms.RadioSelect(),
            'usability': forms.RadioSelect(),
            'content': forms.RadioSelect(),
            'overall': forms.RadioSelect(),
            'description': forms.Textarea(
                attrs={'rows': 4, 'placeholder': 'Add your comments or feedback here.'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        design = cleaned_data.get("design")
        usability = cleaned_data.get("usability")
        content = cleaned_data.get("content")

        if not 1 <= design <= 10:
            self.add_error('design', 'Rating should be between 1 and 10.')
        if not 1 <= usability <= 10:
            self.add_error('usability', 'Rating should be between 1 and 10.')
        if not 1 <= content <= 10:
            self.add_error('content', 'Rating should be between 1 and 10.')

        return cleaned_data

class ProfileForm(forms.ModelForm):
    """ Profile update form """
    class Meta:
        """Class Meta"""
        model = Profile
        fields = ['profile_picture', 'bio',
                  'contact_info', 'location', 
                  'github', 'linkedin', 
                  'twitter', 'instagram', 
                  'facebook', 'profession']

    github = forms.URLField(required=False)
    linkedin = forms.URLField(required=False)
    twitter = forms.URLField(required=False)
    facebook = forms.URLField(required=False)
    instagram = forms.URLField(required=False)

    def clean_github(self):
        """ URL validation """
        github = self.cleaned_data.get('github')

        if not github.startswith(('http://', 'https://')):
            raise ValidationError("The URL must start with 'http://' or 'https://'")

        parsed_github = urlparse(github)
        if not parsed_github.netloc:
            raise ValidationError("The URL must be a valid URL.")

        return github

    def clean_linkedin(self):
        """ URL validation """
        linkedin = self.cleaned_data.get('linkedin')

        if not linkedin.startswith(('http://', 'https://')):
            raise ValidationError("The URL must start with 'http://' or 'https://'")

        parsed_linkedin = urlparse(linkedin)
        if not parsed_linkedin.netloc:
            raise ValidationError("The URL must be a valid URL.")

        return linkedin

    def clean_twitter(self):
        """ URL validation """
        twitter = self.cleaned_data.get('twitter')

        if not twitter.startswith(('http://', 'https://')):
            raise ValidationError("The URL must start with 'http://' or 'https://'")

        parsed_twitter = urlparse(twitter)
        if not parsed_twitter.netloc:
            raise ValidationError("The URL must be a valid URL.")

        return twitter

    def clean_facebook(self):
        """ URL validation """
        facebook = self.cleaned_data.get('facebook')

        if not facebook.startswith(('http://', 'https://')):
            raise ValidationError("The URL must start with 'http://' or 'https://'")

        parsed_facebook = urlparse(facebook)
        if not parsed_facebook.netloc:
            raise ValidationError("The URL must be a valid URL.")

        return facebook

    def clean_instagram(self):
        """ URL validation """
        instagram = self.cleaned_data.get('instagram')

        if not instagram.startswith(('http://', 'https://')):
            raise ValidationError("The URL must start with 'http://' or 'https://'")

        parsed_instagram = urlparse(instagram)
        if not parsed_instagram.netloc:
            raise ValidationError("The URL must be a valid URL.")

        return instagram

class ContactForm(forms.ModelForm):
    '''Contact Form'''
    class Meta:
        '''Class Meta'''
        model = Contact
        fields = ['email', 'subject', 'message']

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        subject = cleaned_data.get("subject")
        message = cleaned_data.get("message")

        if email:
            try:
                EmailValidator()(email)
            except ValidationError as exc:
                raise forms.ValidationError(
                    {'email': "Please enter a valid email address."}) from exc

        if subject and len(subject) > 255:
            raise forms.ValidationError(
                {'subject': "Subject must not exceed a length 255 characters."})

        if message and len(message) > 1000:
            raise forms.ValidationError(
                {'message': "Message must not exceed a length 255 characters."})

        return cleaned_data
