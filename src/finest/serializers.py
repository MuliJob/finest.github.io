""" Serializer for Profile and SubmittedWebsite """
from rest_framework import serializers
from .models import Profile, SubmittedWebsite

class SubmittedWebsiteSerializer(serializers.ModelSerializer):
    """
    Serializer for the SubmittedWebsite model.

    This serializer handles the representation of submitted websites, 
    including fields such as title, URL, description, file, submission date, 
    and whether the website is marked as a favorite.
    """
    class Meta:
        """
        Class Meta
        """
        model = SubmittedWebsite
        fields = ['id', 'title', 'url', 'description', 'file', 'submitted_at', 'is_favorite']


class ProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for the Profile model.

    This serializer includes user profile details such as profile picture, bio, 
    and contact information. It also includes related projects posted by the user 
    through the SubmittedWebsite model.
    """
    projects = SubmittedWebsiteSerializer(source='user.submittedwebsite_set', many=True, read_only=True)

    class Meta:
        """
        Class Meta
        """
        model = Profile
        fields = ['id', 'user', 'profile_picture', 'bio', 'contact_info', 'projects']
