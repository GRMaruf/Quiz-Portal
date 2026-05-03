from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from authentication.forms import *

def user_register(request):
    context = {
        'action': 'register'
    }

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        else:
            context['form'] = form
            return render(request, 'forms/auth-base.html', context)

    form = RegisterForm()
    context['form'] = form
    return render(request, 'forms/auth-base.html', context)

def user_login(request):
    context = {
        'action': 'login',
        'is_login': True
    }

    if request.method == 'POST':
        form = LoginForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
        else:
            context['form'] = form
            return render(request, 'forms/auth-base.html', context)

    form = LoginForm()
    context['form'] = form
    return render(request, 'forms/auth-base.html', context)

@login_required
def user_logout(request):
    logout(request)
    return redirect('home')