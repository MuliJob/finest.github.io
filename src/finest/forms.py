from django import forms
from .models import SubmittedWebsite
import os

class SubmittedWebsiteForm(forms.ModelForm):
    class Meta:
        model = SubmittedWebsite
        fields = ['title', 'url', 'description', 'file']

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if len(title) > 255:
            raise forms.ValidationError("The title should not exceed 255 characters.")
        return title

    def clean_url(self):
        url = self.cleaned_data.get('url')
        if not url.startswith("https://tailwindcss.com/"):
            raise forms.ValidationError("The URL must be in the format https://tailwindcss.com/")
        return url

    def clean_file(self):
        file = self.cleaned_data.get('file')
        max_size_kb = 5000
        allowed_extensions = ['.html', '.htm']
        ext = os.path.splitext(file.name)[1].lower()

        if file.size > max_size_kb * 1024:
            raise forms.ValidationError("File size cannot exceed 5 MB.")
        if ext not in allowed_extensions:
            raise forms.ValidationError("Only .html or .htm files are allowed.")
        return file
