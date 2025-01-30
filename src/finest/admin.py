"""Admin Models"""
from django.contrib import admin
from .models import Contact, SubmittedWebsite, Review, Profile

# Register your models here.
admin.site.register(Contact)
admin.site.register(SubmittedWebsite)
admin.site.register(Review)
admin.site.register(Profile)
