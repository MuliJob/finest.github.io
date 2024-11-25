from django.shortcuts import render

# Create your views here.
def home(request):
  title = 'Project Reviews Application'
  context = {
    'title':title,
  }
  return render(request, 'home.html', context)

def login(request):
   return render(request, 'registration/login.html')

def register(request):
   return render(request, 'registration/register.html')

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