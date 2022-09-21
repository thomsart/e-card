from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('clients/', views.clients, name='clients'),
    path('clients/add/', views.add_client, name='add_clients'),
    path('clients/<user_id>/delete/', views.delete_client, name='delete_client'),

    path('clients/<user_id>/card/', views.see_card, name='see_card'),
    path('clients/<user_id>/card/add/', views.add_card, name='add_card'),
    path('clients/<user_id>/card/<card_id>/delete/', views.delete_card, name='delete_card'),

]
