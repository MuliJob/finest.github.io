from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import SubmittedWebsite
from .forms import SubmittedWebsiteForm


# Create your views here.
def home(request):
    title = 'Project Reviews Application'
    context = {
      'title':title,
    }
    return render(request, 'home.html', context)

@login_required
def dashboard(request):
    title = 'User Dashboard'
    context = {
      'title':title,
    }
    return render(request, 'user/dashboard.html', context)

@login_required
def my_post(request):
    title = 'MY POSTS'
    user_posts = SubmittedWebsite.objects.filter(user=request.user)
    context = {
      'title': title,
      'user_posts': user_posts,
    }
    return render(request, 'user/my-posts.html', context)

@login_required
def my_post_detail(request, pk):
    
    title = 'Website Details'
    website = get_object_or_404(SubmittedWebsite, pk=pk, user=request.user)
    context = {
      'title': title,
      'website': website,
    }
    return render(request, 'user/website-detail.html', context)

@login_required
def favorite(request):
    title = 'Favorites'
    context = {
      'title':title,
    }
    return render(request, 'user/favorites.html', context)

@login_required
def submit_website(request):
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

def contactus(request):
    title = 'Contact Us'
    context = {
      'title':title,
    }
    return render(request, 'contactus.html', context)