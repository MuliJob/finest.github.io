from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import RegisterUserForm

def login_user(request):
  if request.method == 'POST':
    username = request.POST['username']
    password = request.POST["password"]
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        messages.success(request, 'Login Successful.')
        return redirect('dashboard')
    else:
      messages.error(request, 'There was an error logging you in. Please try again.')
      return redirect('login')
  else:
    return render(request, 'auth/login.html', {})
  
def logout_user(request):
  logout(request)
  messages.success(request, 'Logged Out Successful.')
  return redirect('login')

def register_user(request):
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Registration successful.')
                return redirect('dashboard')
    else:
        form = RegisterUserForm()

    return render(request, 'auth/register.html', {'form': form})
