""" Models creation """
from decimal import Decimal
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.exceptions import ValidationError

# Create your models here.
class SubmittedWebsite(models.Model):
    """ SubmittedWebsite form fields """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    url = models.URLField()
    description = models.TextField(blank=True, null=True)
    file = models.FileField(upload_to='uploads/websites/')
    submitted_at = models.DateTimeField(auto_now_add=True)
    is_favorite = models.BooleanField(default=False)
    date_site_of_the_day = models.DateField(blank=True, null=True)

    objects = models.Manager()

class Profile(models.Model):
    """User Profile model"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    profile_picture = models.ImageField(upload_to='uploads/profiles/', blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    contact_info = models.CharField(max_length=255, blank=True, null=True)

    objects = models.Manager()

class Contact(models.Model):
    '''Contact Model'''
    email = models.EmailField(blank=False, null=False)
    subject = models.CharField(max_length=255, blank=False, null=False)
    message = models.TextField(blank=False, null=False)

class Review(models.Model):
    """Review model"""
    design = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 11)], default=1)
    usability = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 11)], default=1)
    content = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 11)], default=1)
    overall = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)], default=1)
    average = models.DecimalField(max_digits=3, decimal_places=2, default=1.0)
    description = models.TextField(blank=True, null=True)
    submitted_website = models.ForeignKey(SubmittedWebsite, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)

    objects = models.Manager()

    def save(self, *args, **kwargs):
        self.average = round(
            Decimal((self.design + self.usability + self.content + self.overall) / 4), 2
        )
        super().save(*args, **kwargs)

    def clean(self):
        for field in ["design", "usability", "content"]:
            value = getattr(self, field)
            if not 1 <= value <= 10:
                raise ValidationError({field: "Rating must be between 1 and 10."})

    def __str__(self):
        username = self.user.username if self.user and hasattr(self.user, 'username') else "Unknown User"
        website = self.submitted_website or "Unknown Website"
        return f"Review by {username} for {website} ({self.average}/5)"