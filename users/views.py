from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
#from django.contrib.auth.views import LoginView
from .models import UserFeedback
from .forms import RegisterForm, LoginForm, FeedbackForm
from django.contrib.auth.views import (
    PasswordResetView, 
    PasswordResetDoneView, 
    PasswordResetConfirmView,
    PasswordResetCompleteView
)

# Create your views here.
def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # autentificăm automat după înregistrare
            return redirect('dashboard')  # redirecționează la pagina de start
    else:
        form = RegisterForm()
    return render(request, 'users/register.html', {'form': form})


def login_view(request):
    form = LoginForm(request=request, data=request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                messages.success(request, f'{user.username.title()}, bine ai revenit!')
                return redirect('homepage')
        # fie autentificarea a eșuat, fie formularul nu e valid
        messages.error(request, 'Nume de utilizator sau parolă incorectă.')
    return render(request, 'users/login.html', {'form': form})

def signout_view(request):
    logout(request)
    messages.info(request, "Te-ai deconectat cu succes. Ne revedem curând! 👋")
    return redirect('homepage')     

@login_required
def feedback_view(request):
    form = FeedbackForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.user = request.user
            feedback.save()
            messages.success(request, "Mulțumim pentru feedback!")
            return redirect('dashboard')  # sau oriunde dorești
    return render(request, 'users/feedback.html', {'form': form})

@login_required
def dashboard_view(request):
    return render(request, 'users/dashboard.html')

def homepage_view(request):
    return render(request, 'users/homepage.html')

@login_required
def profile_view(request):
    return render(request, 'users/profile.html')

def termeni_view(request):
    return render(request, 'users/termeni.html')

