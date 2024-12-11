""" Finest app views """
import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.views import redirect_to_login
from django.urls import reverse
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from .models import SubmittedWebsite, Review
from .forms import SubmittedWebsiteForm, ReviewForm



# Create your views here.
def custom_login_required(view_func):
    """ Custom login required decorator to add a message on redirect """
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, "You need to be logged in to access this page. Please login below!")
            login_url = reverse('login')
            return redirect_to_login(request.get_full_path(), login_url)
        return view_func(request, *args, **kwargs)
    return wrapper

def home(request):
    """ Homepage function """
    highest_avg_review = Review.objects.order_by('-average').first()

    if highest_avg_review:
        website = highest_avg_review.submitted_website
        formatted_date = highest_avg_review.created_at.strftime('%b %d, %Y')

        alt_name = website.title if website.title else "Website Image"

        context = {
            'title': 'Project Reviews Application',
            'website_title': website.title,
            'website_image': website.file.url if website.file else None,
            'website_description': website.description,
            'review_score': highest_avg_review.average,
            'formatted_date': formatted_date,
            'alt_name': alt_name
        }
    else:
        context = {
            'title': 'Project Reviews Application',
            'message': "No reviews available yet"
        }

    return render(request, 'home.html', context)

@custom_login_required
def dashboard(request):
    """ User dashboard """
    title = 'User Dashboard'
    context = {
      'title':title,
    }
    return render(request, 'user/dashboard.html', context)

@custom_login_required
def my_post(request):
    """ Posted websites """
    title = 'MY POSTS'
    user_posts = SubmittedWebsite.objects.filter(user=request.user)
    context = {
      'title': title,
      'user_posts': user_posts,
    }
    return render(request, 'user/my-posts.html', context)

@custom_login_required
def my_post_detail(request, pk):
    """ Posted website details """
    title = 'Website Details'
    website = get_object_or_404(SubmittedWebsite, pk=pk, user=request.user)

    reviews = website.reviews.all()

    total_reviews = reviews.count() if reviews.exists() else 0

    if reviews.exists():
        overall_rating = reviews.first().overall
    else:
        overall_rating = 0

    context = {
      'title': title,
      'website': website,
      'reviews': reviews,
      'total_reviews': total_reviews,
      'overall_rating': overall_rating,
    }
    return render(request, 'user/website-detail.html', context)

@custom_login_required
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

@custom_login_required
def favorite(request):
    """ Favorites function """
    title = 'FAVORITES'

    favorites = SubmittedWebsite.objects.filter(user=request.user, is_favorite=True)

    context = {
      'title': title,
      'favorites': favorites,
    }
    return render(request, 'user/favorites.html', context)

@custom_login_required
def add_review(request, pk):
    """Adding review function"""
    submitted_website = get_object_or_404(SubmittedWebsite, id=pk)

    if Review.objects.filter(submitted_website=submitted_website, user=request.user).exists():
        messages.error(request, 'You have already reviewed this website.')
        return redirect('my_post_detail', pk=pk)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.submitted_website = submitted_website
            review.user = request.user
            review.save()

            messages.success(request, 'Your review has been added successfully.')
            return redirect('my_post_detail', pk=pk)
        else:
            messages.error(request, 'Form validation failed. Please try again.')
            return redirect('my_post_detail', pk=pk)

    messages.error(request, 'Only POST requests are allowed.')
    return redirect('my_post_detail', pk=pk)


@custom_login_required
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