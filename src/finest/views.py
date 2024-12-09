from django.shortcuts import render, redirect
from .forms import SubmittedWebsiteForm
from django.contrib.auth.decorators import login_required


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
    title = 'My Posts'
    context = {
      'title':title,
    }
    return render(request, 'user/my-posts.html', context)

@login_required
def my_post_detail(request):
    title = 'Website Details'
    context = {
      'title':title,
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
    title = 'Submit Website'

    if request.method == 'POST':
        form = SubmittedWebsiteForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('my_post')
        else:
            context = {
                'title': title,
                'form': form,
            }
            return render(request, 'user/submit-website.html', context)
    else:
        form = SubmittedWebsiteForm()

    context = {
        'title': title,
        'form': form,
    }
    return render(request, 'user/submit-website.html', context)

def contactus(request):
    title = 'Contact Us'
    context = {
      'title':title,
    }
    return render(request, 'contactus.html', context)