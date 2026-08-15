from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.list_houses, name='list_houses'),
    path('adauga/', views.add_house, name='add_house'),
    path('actualizeaza/<int:pk>/', views.edit_house, name='edit_house'),
    path('sterge/<int:pk>/', views.delete_house, name='delete_house'),
    path('detail/<int:pk>/', views.detail_house, name='detail_house'),
    path('search/', views.search_houses, name='search_houses'),
    path('alerts_view', views.alerts_view, name='alerts_view'),
    path('statistics_view', views.statistics_view, name='statistics_view'),
    path('add_todo', views.add_todo, name='add_todo'),
    #path('edit_contabil', views.edit_contabil, name='edit_contabil'),
    path('adauga_operatiune/', views.adauga_operatiune, name='adauga_operatiune'),
    path('lista_operatiuni/', views.lista_operatiuni, name='lista_operatiuni'),
    path('download_house_txt/<int:pk>/', views.download_house_txt, name='download_house_txt'),
    path('download_houses_zip', views.download_houses_zip, name='download_houses_zip'),
    path('add_treatment', views.add_treatment, name='add_treatment'),
    path('genereaza_fisele', views.genereaza_fisele, name='genereaza_fisele'),
    path('add_visit/<int:pk>', views.add_visit, name='add_visit'),
    path('bifeaza/<int:pk>/', views.bifare_view, name='bifare_view'),
    path('debifeaza/<int:pk>/', views.debifare_view, name='debifare_view'),
    path('pastoral_view/', views.pastoral_view, name='pastoral_view'),
    path('delete_pastoral/<int:pk>', views.delete_pastoral, name='delete_pastoral'),
]