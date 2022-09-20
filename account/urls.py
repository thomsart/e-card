from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('clients/', views.clients, name='clients'),
    path('clients/add/', views.add_client, name='add_clients'),
    path('clients/card/add/', views.add_card, name='add_card'),
    path('clients/card/delete/', views.delete_card, name='delete_card'),
    path('clients/delete/', views.delete_client, name='delete_client'),

    path('clients/get_card/', views.get_card, name='get_card'),
]
