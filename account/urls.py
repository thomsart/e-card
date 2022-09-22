from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('clients/', views.clients, name='clients'),
    path('clients/add/', views.add_client, name='add_clients'),
    path('clients/<user_id>/delete/', views.delete_client, name='delete_client'),
]
