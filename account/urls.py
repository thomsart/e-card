from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('register/', views.user_register, name='user_register'),
    path('login/', views.user_login, name='user_login'),
    path('logout/', views.user_logout, name='user_logout'),
    path('clients/', views.clients, name='clients'),
    path('clients/add/', views.add_client, name='add_clients'),
    path('clients/<user_id>/desactivate/', views.desactivate_reactivate_client, name='desactivate_reactivate_client'),
    path('clients/<user_id>/delete/', views.delete_client, name='delete_client'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
