""" Form creation and validation """
from urllib.parse import urlparse
import os
from django import forms
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError
from .models import Contact, SubmittedWebsite, Review, Profile

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
        fields = ['design', 'usability', 'content', 'overall', 'description']  # Include 'description' field
        widgets = {
            'design': forms.RadioSelect(),
            'usability': forms.RadioSelect(),
            'content': forms.RadioSelect(),
            'overall': forms.RadioSelect(),
            'description': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Add your comments or feedback here.'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        design = cleaned_data.get("design")
        usability = cleaned_data.get("usability")
        content = cleaned_data.get("content")

        # Ensure ratings are within the valid range
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
        fields = ['profile_picture', 'bio', 'contact_info']

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
                raise ValidationError("Please enter a valid email address.") from exc

        if subject and len(subject) > 255:
            raise ValidationError("Subject must not exceed 255 characters.")
        if not subject:
            raise ValidationError("Subject is required.")

        if not message:
            raise ValidationError("Message cannot be empty.")

        return cleaned_data
