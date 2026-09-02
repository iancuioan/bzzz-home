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
from django.contrib.auth.models import User

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

def demo_login_view(request):
    """Loghează automat utilizatorul 'demo' fără formular."""
    DEMO_USERNAME = "demo"

    try:
        # get_or_create previne eroarea User.DoesNotExist pe baza de date nouă (Supabase)
        user, created = User.objects.get_or_create(
            username=DEMO_USERNAME,
            defaults={
                "email": "demo@example.com",
                "is_active": True,
            },
        )

        if created:
            user.set_unusable_password()
            user.save()

        # Atașăm backend-ul pentru a evita AttributeError la login() direct
        user.backend = "django.contrib.auth.backends.ModelBackend"

        login(request, user)
        messages.info(
            request, "Te-ai logat pe contul de DEMO (mod doar vizualizare)."
        )
        return redirect("homepage")

    except Exception as e:
        messages.error(
            request, f"Eroare la autentificarea pe contul demo: {str(e)}"
        )
        return redirect("login")