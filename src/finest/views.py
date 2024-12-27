""" Finest app views """
import json
from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.views import redirect_to_login
from django.urls import reverse
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.db.models import Avg
from django.contrib.auth.models import User
from .models import SubmittedWebsite, Review, Profile
from .forms import SubmittedWebsiteForm, ReviewForm, ProfileForm
from .serializers import ProfileSerializer, SubmittedWebsiteSerializer
from .permissions import IsAdminOrReadOnly



# Create your views here.
class ProfileListAPIView(generics.ListAPIView):
    """API endpoint for retrieving all user profiles."""
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['user']

    permission_classes = (IsAdminOrReadOnly,)

class SubmittedWebsiteListAPIView(generics.ListAPIView):
    """
    API endpoint for retrieving all projects.
    """
    queryset = SubmittedWebsite.objects.all()
    serializer_class = SubmittedWebsiteSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['user', 'is_favorite']

    permission_classes = (IsAdminOrReadOnly,)

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
            'title': 'FINEST',
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
    title = 'USER DASHBOARD'
    total_projects = SubmittedWebsite.objects.filter(user=request.user).count()
    reviewed_projects_count = SubmittedWebsite.objects.filter(user=request.user, reviews__isnull=False).distinct().count()
    non_reviewed_projects_count = total_projects - reviewed_projects_count
    average_review_score = (
        Review.objects.filter(submitted_website__user=request.user)
        .aggregate(avg_score=Avg('overall'))['avg_score'] or 0
    )

    context = {
        'title': title,
        'total_projects': total_projects,
        'reviewed_projects_count': reviewed_projects_count,
        'non_reviewed_projects_count': non_reviewed_projects_count,
        'average_review_score': round(average_review_score, 1),
    }

    return render(request, 'user/dashboard.html', context)

@custom_login_required
def explore(request):
    """Explore Page - Top Rated Projects"""
    title = 'EXPLORE'
    top_rated_projects = SubmittedWebsite.objects.annotate(
        avg_score=Avg('reviews__average')
    ).order_by('-avg_score')[:5]

    highest_design = SubmittedWebsite.objects.annotate(
        design_score=Avg('reviews__design')
    ).order_by('-design_score')[:5]

    highest_content = SubmittedWebsite.objects.annotate(
        content_score=Avg('reviews__content')
    ).order_by('-content_score')[:5]

    highest_usability = SubmittedWebsite.objects.annotate(
        usability_score=Avg('reviews__usability')
    ).order_by('-usability_score')[:5]

    context = {
        'title': title,
        'top_rated_projects': top_rated_projects,
        'highest_design': highest_design,
        'highest_content': highest_content,
        'highest_usability': highest_usability,
    }

    return render(request, 'user/explore.html', context)

@custom_login_required
def my_post(request):
    """ Posted websites """
    title = 'MY POSTS'
    user_posts = SubmittedWebsite.objects.filter(user=request.user).annotate(
        highest_rating=Avg('reviews__overall')
    )
    context = {
      'title': title,
      'user_posts': user_posts,
    }
    return render(request, 'user/my-posts.html', context)

@custom_login_required
def my_post_detail(request, pk):
    """ Posted website details """
    title = 'WEBSITE DETAILS'
    website = get_object_or_404(SubmittedWebsite, pk=pk, user=request.user)
    is_submitted_by_user = website.user == request.user
    has_user_reviewed = Review.objects.filter(
        submitted_website=website, user=request.user
    ).exists()

    reviews = website.reviews.all()

    total_reviews = reviews.count() if reviews.exists() else 0

    if reviews.exists():
        overall_rating = reviews.aggregate(max_rating=Avg('overall'))['max_rating']
    else:
        overall_rating = 0

    context = {
      'title': title,
      'website': website,
      'reviews': reviews,
      'total_reviews': total_reviews,
      'overall_rating': overall_rating,
      'is_submitted_by_user': is_submitted_by_user,
      'has_user_reviewed': has_user_reviewed,
    }
    return render(request, 'user/website-detail.html', context)

@custom_login_required
def all_post_details(request, pk):
    """ All posted website details for all users """
    title = 'WEBSITE DETAILS'
    
    website = get_object_or_404(SubmittedWebsite, pk=pk)
    
    has_user_reviewed = Review.objects.filter(
        submitted_website=website, user=request.user
    ).exists()

    reviews = website.reviews.all()

    total_reviews = reviews.count() if reviews.exists() else 0

    if reviews.exists():
        overall_rating = reviews.aggregate(max_rating=Avg('overall'))['max_rating']
    else:
        overall_rating = 0

    context = {
      'title': title,
      'website': website,
      'reviews': reviews,
      'total_reviews': total_reviews,
      'overall_rating': overall_rating,
      'has_user_reviewed': has_user_reviewed,
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

    favorites = SubmittedWebsite.objects.filter(user=request.user, is_favorite=True).annotate(
        highest_rating = Avg('reviews__overall')
    )

    context = {
      'title': title,
      'favorites': favorites,
    }
    return render(request, 'user/favorites.html', context)

@custom_login_required
def add_review(request, pk):
    """Allow users to add a review to a project they did not submit."""
    submitted_website = get_object_or_404(SubmittedWebsite, id=pk)

    if submitted_website.user == request.user:
        messages.error(request, 'You cannot review your own project.')
        return redirect('all_post_details', pk=pk)

    if Review.objects.filter(submitted_website=submitted_website, user=request.user).exists():
        messages.error(request, 'You have already reviewed this project.')
        return redirect('all_post_details', pk=pk)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.submitted_website = submitted_website
            review.user = request.user
            review.save()

            messages.success(request, 'Your review has been added successfully.')
            return redirect('all_post_details', pk=pk)
        else:
            messages.error(request, 'Invalid data. Please correct the errors and try again.')
            return redirect('all_post_details', pk=pk)

    messages.error(request, 'Only POST requests are allowed for adding reviews.')
    return redirect('all_post_details', pk=pk)


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

@custom_login_required
def edit_profile(request, username):
    """View to edit user profile"""
    user = get_object_or_404(User, username=username)
    
    if request.user != user:
        messages.error(request, "You are not authorized to edit this profile.")
        return redirect('home')
    profile, _ = Profile.objects.get_or_create(user=user)

    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect('edit_profile', username=user.username)
        else:
            messages.error(request, "There was an error updating your profile.")
    else:
        form = ProfileForm(instance=profile)

    context = {
        'title': f"Edit Profile - {user.username}",
        'form': form,
        'profile': profile,
    }
    return render(request, 'user/profile.html', context)

def contact_us(request):
    """ Contact function"""
    title = 'CONTACT US'
    context = {
      'title':title,
    }
    return render(request, 'contactus.html', context)