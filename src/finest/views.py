""" Finest app views """
import json
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import SubmittedWebsite
from .forms import SubmittedWebsiteForm



# Create your views here.
def home(request):
    """ Homepage function """
    title = 'Project Reviews Application'
    context = {
      'title':title,
    }
    return render(request, 'home.html', context)

@login_required
def dashboard(request):
    """ User dashboard """
    title = 'User Dashboard'
    context = {
      'title':title,
    }
    return render(request, 'user/dashboard.html', context)

@login_required
def my_post(request):
    """ Posted websites """
    title = 'MY POSTS'
    user_posts = SubmittedWebsite.objects.filter(user=request.user)
    context = {
      'title': title,
      'user_posts': user_posts,
    }
    return render(request, 'user/my-posts.html', context)

@login_required
def my_post_detail(request, pk):
    """ Posted website details """
    title = 'Website Details'
    website = get_object_or_404(SubmittedWebsite, pk=pk, user=request.user)
    context = {
      'title': title,
      'website': website,
    }
    return render(request, 'user/website-detail.html', context)

@login_required
def toggle_favorite(request):
    """ Toggling favorite """
    if request.method == 'POST':
        data = json.loads(request.body)
        website_id = data.get('website_id')

        if not website_id:
            return JsonResponse({"success": False, "error": "Missing website ID"}, status=400)

        try:
            website = SubmittedWebsite.objects.get(id=website_id, user=request.user)
            is_favorite = not website.is_favorite
            website.is_favorite = is_favorite
            website.save()
            return JsonResponse({"success": True, "is_favorite": is_favorite})
        except ObjectDoesNotExist:
            return JsonResponse({"success": False, "error": "Website not found"}, status=404)
    return JsonResponse({"success": False, "error": "Invalid request method"}, status=405)

@login_required
def favorite(request):
    """ Favorites function """
    title = 'FAVORITES'
    context = {
      'title': title,
    }
    return render(request, 'user/favorites.html', context)

@login_required
def submit_website(request):
    """ Submitting website """
    if request.method == 'POST':
        form = SubmittedWebsiteForm(request.POST, request.FILES)
        if form.is_valid():
            submitted_website = form.save(commit=False)
            submitted_website.user = request.user
            submitted_website.save()
            messages.success(request, "Your website was submitted successfully.")
            return redirect('my_post')
        else:
            messages.error(request, "There was an error with your submission. Please correct it below.")
    else:
        form = SubmittedWebsiteForm()

    context = {
        'title': 'SUBMIT WEBSITE',
        'form': form,
    }
    return render(request, 'user/submit-website.html', context)

def contact_us(request):
    """ Contact function"""
    title = 'Contact Us'
    context = {
      'title':title,
    }
    return render(request, 'contactus.html', context)