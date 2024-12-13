""" Members app authentication view functions """
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import RegisterUserForm, LoginUserForm

def login_user(request):
    """Login user function"""
    if request.method == 'POST':
        form = LoginUserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                messages.success(request, f'Login Successful. Welcome {username}')
                return redirect('dashboard')
        else:
            return render(request, 'auth/login.html', {'form': form})
    else:
        form = LoginUserForm()
    return render(request, 'auth/login.html', {'form': form})

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
