"""
from django.shortcuts import redirect
from django.urls import reverse

class RedirectAuthenticatedUserMiddleware:
    PUBLIC_PATHS = [
        'login',
        'register',
        'password_reset',
        'password_reset_confirm',
        'password_reset_complete',
        'password_reset_done',
        'homepage',
    ]
    PROTECTED_PATHS = ['dashboard']

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        current_path = request.path

        # Dacă e logat și intră pe o pagină publică → du-l la dashboard
        if request.user.is_authenticated:
            for path_name in self.PUBLIC_PATHS:
                if current_path == reverse(path_name):
                    return redirect('dashboard')

        # Dacă NU e logat și intră pe o pagină protejată → trimite-l la login
        else:
            for path_name in self.PROTECTED_PATHS:
                if current_path == reverse(path_name):
                    return redirect('login')

        return self.get_response(request)
"""
from django.contrib import messages
from django.shortcuts import redirect

class DemoUserProtectionMiddleware:
    """
    Blochează acțiunile de modificare (POST, PUT, DELETE) 
    pentru contul de demo.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Specifică username-ul contului de demo
        DEMO_USERNAME = 'demo'

        if request.user.is_authenticated and request.user.username == DEMO_USERNAME:
            # Permite doar vizualizarea (GET, HEAD, OPTIONS)
            if request.method not in ['GET', 'HEAD', 'OPTIONS']:
                messages.warning(
                    request, 
                    "Sunteți în modul DEMO. Acțiunile de adăugare, editare sau ștergere sunt dezactivate."
                )
                # Redirecționează utilizatorul la pagina de unde a încercat să facă acțiunea
                return redirect(request.META.get('HTTP_REFERER', '/'))

        response = self.get_response(request)
        return response