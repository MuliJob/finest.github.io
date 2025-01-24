""" Finest app views """
import json
from datetime import timedelta, datetime
from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.views import redirect_to_login
from django.urls import reverse
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.db.models import Avg, Count
from django.db.models.functions import TruncMonth
from django.contrib.auth.models import User
from django.utils.timezone import now
from .models import SubmittedWebsite, Review, Profile
from .forms import ContactForm, SubmittedWebsiteForm, ReviewForm, ProfileForm
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
            messages.warning(request,
                             "You need to be logged in to access this page. Please login below!")
            login_url = reverse('login')
            return redirect_to_login(request.get_full_path(), login_url)
        return view_func(request, *args, **kwargs)
    return wrapper

def performance_chart(request):
    """Function to display user review project"""
    current_year = datetime.now().year

    review_data = (
        Review.objects.filter(user=request.user, created_at__year=current_year)
        .annotate(month=TruncMonth('created_at'))
        .values('month')
        .annotate(total_reviews=Count('id'))
        .order_by('month')
    )

    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    data = {month: 0 for month in months}

    for item in review_data:
        month_index = item['month'].month - 1
        data[months[month_index]] = item['total_reviews']

    filtered_labels = [month for month, count in data.items() if count > 0]
    filtered_data = [count for month, count in data.items() if count > 0]

    return render(request, 'chart.html', {
        'labels': filtered_labels,
        'data': filtered_data,
    })

def home(request):
    """Homepage function"""
    project_avg_reviews = (
        Review.objects.values('submitted_website', 'submitted_website__title')
        .annotate(average_per_user=Avg('average'))
        .order_by('-average_per_user')
    )

    highest_avg_review = project_avg_reviews.first()

    if highest_avg_review:
        website_id = highest_avg_review['submitted_website']
        website = SubmittedWebsite.objects.get(id=website_id)
        formatted_date = now().strftime('%b %d, %Y')

        alt_name = website.title if website.title else "Website Image"
        user = website.user

        profile = getattr(user, 'profile', None)
        profile_picture = (
            profile.profile_picture.url if profile and profile.profile_picture else None
        )

        context = {
            'title': 'FINEST',
            'website_title': website.title,
            'website_image': website.file.url if website.file else None,
            'website_description': website.description,
            'review_score': highest_avg_review['average_per_user'],
            'formatted_date': formatted_date,
            'alt_name': alt_name,
            'user_username': user.username,
            'user_profile_url': f'/profile/{user.username}/',
            'user_avatar_url': profile_picture or f'https://robohash.org/{user.username}.png?size=96x96',
        }
    else:
        context = {
            'title': 'Project Reviews Application',
            'message': "No reviews available yet"
        }

    today = now().date()

    recent_sites = (
        SubmittedWebsite.objects.filter(date_site_of_the_day__lt=today)
        .order_by('-date_site_of_the_day')[:6]
    )

    for i in range(1, 7):
        day = today - timedelta(days=i)
        if not SubmittedWebsite.objects.filter(date_site_of_the_day=day).exists():
            highest_rating_for_day = (
                Review.objects.filter(created_at__date=day)
                .values('submitted_website')
                .annotate(average_per_user=Avg('average'))
                .order_by('-average_per_user')
                .first()
            )
            if highest_rating_for_day:
                site = SubmittedWebsite.objects.get(id=highest_rating_for_day['submitted_website'])
                site.date_site_of_the_day = day
                site.save()

    context['recent_sites'] = recent_sites

    return render(request, 'home.html', context)


@custom_login_required
def dashboard(request):
    """ User dashboard """
    title = 'USER DASHBOARD'
    total_projects = SubmittedWebsite.objects.filter(user=request.user).count()
    reviewed_projects_count = (SubmittedWebsite.objects
                               .filter(user=request.user, reviews__isnull=False)
                               .distinct().count())
    non_reviewed_projects_count = total_projects - reviewed_projects_count
    average_review_score = (
        Review.objects.filter(submitted_website__user=request.user)
        .aggregate(avg_score=Avg('overall'))['avg_score'] or 0
    )
    recent_projects = (SubmittedWebsite.objects
                       .filter(user=request.user)
                       .order_by('-submitted_at')[:4])

    top_review = Review.objects.filter(
        user=request.user,
        submitted_website__user=request.user
    ).order_by('-average').first()

    if top_review:
        top_feedback = top_review.description or "No feedback available yet."
        top_feedback_id = top_review.submitted_website.pk
    else:
        top_feedback = "No feedback available yet."
        top_feedback_id = None

    lowest_review = (Review.objects.filter(
        user=request.user,
        submitted_website__user=request.user
    ).order_by('average').first())

    if lowest_review:
        improvement_tip = lowest_review.description or "No improvement tips available yet."
        improvement_project_id = lowest_review.submitted_website.pk
    else:
        improvement_tip = "No improvement tips available yet."
        improvement_project_id = None

    current_hour = datetime.now().hour
    if current_hour < 12:
        greeting = "Good Morning"
    elif current_hour < 18:
        greeting = "Good Afternoon"
    else:
        greeting = "Good Evening"

    current_year = datetime.now().year

    review_data = (
        Review.objects.filter(user=request.user, created_at__year=current_year)
        .annotate(month=TruncMonth('created_at'))
        .values('month')
        .annotate(total_reviews=Count('id'))
        .order_by('month')
    )

    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    data = {month: 0 for month in months}

    for item in review_data:
        month_index = item['month'].month - 1
        data[months[month_index]] = item['total_reviews']

    filtered_labels = [month for month, count in data.items() if count > 0]
    filtered_data = [count for month, count in data.items() if count > 0]

    recent_submissions = (SubmittedWebsite
                          .objects
                          .filter(user=request.user)
                          .order_by('-submitted_at')[:2])

    context = {
        'title': title,
        'total_projects': total_projects,
        'reviewed_projects_count': reviewed_projects_count,
        'non_reviewed_projects_count': non_reviewed_projects_count,
        'average_review_score': round(average_review_score, 1),
        'recent_projects': recent_projects,
        'top_feedback': top_feedback,
        'top_feedback_id': top_feedback_id,
        'improvement_tip': improvement_tip,
        'improvement_project_id': improvement_project_id,
        'greeting': greeting,
        'labels': json.dumps(filtered_labels),
        'data': json.dumps(filtered_data),
        'recent_submissions': recent_submissions,
    }

    return render(request, 'user/dashboard.html', context)

@custom_login_required
def explore(request):
    """Explore Page - Top Rated Projects"""
    title = 'EXPLORE'

    all_projects = SubmittedWebsite.objects.order_by('-submitted_at')[:5]

    top_rated_projects = (
        SubmittedWebsite.objects.annotate(
            avg_user_score=Avg('reviews__average', distinct=True)
        )
        .filter(reviews__isnull=False)
        .order_by('-avg_user_score')[:5]
    )

    highest_design = (
        SubmittedWebsite.objects.annotate(
            avg_design_score=Avg('reviews__design', distinct=True)
        )
        .filter(reviews__isnull=False)
        .order_by('-avg_design_score')[:5]
    )

    highest_content = (
        SubmittedWebsite.objects.annotate(
            avg_content_score=Avg('reviews__content', distinct=True)
        )
        .filter(reviews__isnull=False)
        .order_by('-avg_content_score')[:5]
    )

    highest_usability = (
        SubmittedWebsite.objects.annotate(
            avg_usability_score=Avg('reviews__usability', distinct=True)
        )
        .filter(reviews__isnull=False)
        .order_by('-avg_usability_score')[:5]
    )

    context = {
        'title': title,
        "all_projects": all_projects,
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
    user_posts = (SubmittedWebsite.objects
                  .filter(user=request.user)
                  .order_by('-submitted_at')
                  .annotate(highest_rating=Avg('reviews__overall')
    ))
    context = {
      'title': title,
      'user_posts': user_posts,
    }
    return render(request, 'user/my-posts.html', context)

@custom_login_required
def my_reviews(request):
    '''My Reviews Function'''
    title = 'My Reviews'
    reviews = Review.objects.filter(user=request.user).order_by('-created_at')
    context = {
        'title': title,
        'reviews': reviews,
    }
    return render(request, 'user/my-reviews.html', context)

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
def toggle_favorite(request):
    """ Toggling favorite for any website """
    if request.method == 'POST':
        data = json.loads(request.body)
        website_id = data.get('website_id')

        if not website_id:
            return JsonResponse({"success": False, "error": "Missing website ID"}, status=400)

        try:
            website = SubmittedWebsite.objects.get(id=website_id)

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
            messages.error(request, 
                           "There was an error with your submission. Please correct it below.")
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
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact_info = form.save(commit=False)
            contact_info.save()
            messages.success(request,
                            'We have received your message 🤝. We will contact you soon. 🤖')
        else:
            messages.error(request,
                           "There was an error with your submission. Please correct it below.")
    else:
        form = ContactForm
    context = {
      'title':title,
      'form': form,
    }
    return render(request, 'contactus.html', context)
