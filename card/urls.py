from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('clients/<user_id>/card/', views.get_card, name='get_card'),
    path('clients/<user_id>/card/add/', views.add_card, name='add_card'),
    path('clients/<user_id>/card/<card_id>/delete/', views.delete_card, name='delete_card'),
]
