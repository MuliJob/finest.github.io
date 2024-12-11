""" Members app authentication view functions """
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import RegisterUserForm

def login_user(request):
    """ Login user function """
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not User.objects.filter(username=username).exists():
            messages.error(request, 'The username does not exist. Please try again.')
            return redirect('login')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Login Successful.')
            return redirect('dashboard')
        else:
            messages.error(request, 'Incorrect password. Please try again.')
            return redirect('login')
    else:
        return render(request, 'auth/login.html', {})

def logout_user(request):
    """ Logout user function """
    logout(request)
    messages.success(request, 'Logged Out Successful.')
    return redirect('login')

def register_user(request):
    """ User registration function """
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Registration successful. Welcome {username}!')
                return redirect('dashboard')
            else:
                messages.error(request, 'Registration successful, but we couldn\'t log you in. Please log in manually.')
    else:
        form = RegisterUserForm()

    return render(request, 'auth/register.html', {'form': form})
