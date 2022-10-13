from django.urls import path

from . import views


urlpatterns = [
    path('register/', views.user_register, name='user_register'),
    path('login/', views.user_login, name='user_login'),
    path('logout/', views.user_logout, name='user_logout'),
    path('', views.home, name='home'),
    path('client/add/', views.add_client, name='add_client'),
    path('client/<user_id>/desactivate/', views.deactivate_reactivate_client, name='desactivate_reactivate_client'),
    path('client/<user_id>/delete/', views.delete_client, name='delete_client'),
]