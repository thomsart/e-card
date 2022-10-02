from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('clients/', views.clients, name='clients'),
    path('clients/add/', views.add_client, name='add_clients'),
    path('clients/<user_id>/desactive/', views.desactive_client, name='desactive_client'),
    path('clients/<user_id>/delete/', views.delete_client, name='delete_client'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
