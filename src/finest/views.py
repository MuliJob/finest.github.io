from django.shortcuts import render

# Create your views here.
def home(request):
  title = 'Project Reviews Application'
  context = {
    'title':title,
  }
  return render(request, 'home.html', context)

def dashboard(request):
  title = 'User Dashboard'
  context = {
    'title':title,
  }
  return render(request, 'user/dashboard.html', context)

def my_post(request):
  title = 'My Posts'
  context = {
    'title':title,
  }
  return render(request, 'user/my-posts.html', context)

def my_post_detail(request):
  title = 'Website Details'
  context = {
    'title':title,
  }
  return render(request, 'user/website-detail.html', context)

def posted(request):
  title = 'Posted Websites'
  context = {
    'title':title,
  }
  return render(request, 'user/posted.html', context)

def submit_website(request):
  title = 'Submit Website'
  context = {
    'title':title,
  }
  return render(request, 'user/submit-website.html', context)

def contactus(request):
  title = 'Contact Us'
  context = {
    'title':title,
  }
  return render(request, 'contactus.html', context)