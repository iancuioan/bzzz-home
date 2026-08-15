from django.urls import path
from django.contrib.auth import views as auth_views
    
from . import views

urlpatterns = [
    path('', views.homepage_view, name='homepage'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.signout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('termeni/', views.termeni_view, name='termeni'),
    path('feedback/', views.feedback_view, name='feedback'),
    path('profil/', views.profile_view, name='profile'),
    # Resetare parolă
    path('resetare-parola/', 
         auth_views.PasswordResetView.as_view(
             template_name='users/password_reset.html',
             email_template_name='users/password_reset_email.html',
             subject_template_name='users/password_reset_subject.txt',
             success_url='done/'
         ), 
         name='password_reset'),

    path('resetare-parola/done/', 
         auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'), 
         name='password_reset_done'),

    path('resetare-parola/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'), 
         name='password_reset_confirm'),

    path('resetare-parola/complet/', 
         auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'), 
         name='password_reset_complete'),
    # Schimbare parola
    path('schimba-parola/', 
         auth_views.PasswordChangeView.as_view(
             template_name='users/password_change.html',
             success_url='/schimba-parola/complet/'
         ), 
         name='password_change'),

    path('schimba-parola/complet/', 
         auth_views.PasswordChangeDoneView.as_view(
             template_name='users/password_change_done.html'
         ), 
         name='password_change_done'),
    ]
