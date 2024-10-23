# factures/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.accueil, name='accueil'),
    path('factures/', views.liste_factures, name='liste_factures'),
    path('factures/<int:pk>/', views.detail_facture, name='detail_facture'),
    path('factures/creer/', views.creer_facture, name='creer_facture'),
    path('factures/<int:pk>/modifier/', views.modifier_facture, name='modifier_facture'),
    path('factures/<int:pk>/supprimer/', views.supprimer_facture, name='supprimer_facture'),
    path('categories/', views.liste_categories, name='liste_categories'),
    path('categories/<int:categorie_id>/factures/', views.factures_par_categorie, name='factures_par_categorie'),
]