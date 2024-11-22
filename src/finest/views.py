from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import ensure_csrf_cookie

# Create your views here.
@require_POST
def toggle_theme(request):
    current_theme = request.session.get('theme', 'light')
    new_theme = 'dark' if current_theme == 'light' else 'light'
    request.session['theme'] = new_theme
    return JsonResponse({'theme': new_theme})

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