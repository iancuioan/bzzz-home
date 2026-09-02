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
from django.http import JsonResponse
from django.urls import reverse

class DemoUserProtectionMiddleware:
    """Blochează acțiunile de modificare (POST, PUT, PATCH, DELETE) pentru contul de demo."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        DEMO_USERNAME = "demo"

        # Verificăm dacă utilizatorul este autentificat și este pe contul demo
        if (
            request.user.is_authenticated
            and request.user.username == DEMO_USERNAME
        ):
            # Lista de metode sigure (doar citire)
            if request.method not in ["GET", "HEAD", "OPTIONS"]:

                # Excepție 1: Permitem acțiunea de LOGOUT chiar dacă este de tip POST
                logout_url = reverse(
                    "logout"
                )  # Înlocuiește 'logout' cu numele rutei tale dacă diferă
                if request.path == logout_url:
                    return self.get_response(request)

                # Excepție 2: Tratăm cererile de tip AJAX / Fetch / API
                if (
                    request.headers.get("x-requested-with") == "XMLHttpRequest"
                    or "application/json"
                    in request.headers.get("Accept", "")
                ):
                    return JsonResponse(
                        {
                            "error": "Sunteți în modul DEMO. Modificările sunt dezactivate."
                        },
                        status=403,
                    )

                # Pentru cereri standard din formulare HTML: adăugăm mesaj și redirecționăm
                messages.warning(
                    request,
                    "Sunteți în modul DEMO. Acțiunile de adăugare, editare sau ștergere sunt dezactivate.",
                )

                # Folosim HTTP_REFERER cu fallback sigur
                referer = request.META.get("HTTP_REFERER")
                if referer and referer != request.build_absolute_uri():
                    return redirect(referer)
                return redirect("homepage")  # Schimbă cu ruta ta principală

        return self.get_response(request)