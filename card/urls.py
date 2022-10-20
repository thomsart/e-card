from django.urls import path

from . import views

urlpatterns = [
    path('client/<user_id>/card/', views.add_card, name='add_card'),
    path('client/<user_id>/<user_email>/card/<card_id>/', views.get_card, name='get_card'),
    path('client/<user_id>/card/<card_id>/email_link/', views.send_email_link, name='send_email_link'),
    path('client/<user_id>/card/<card_id>/delete/', views.delete_card, name='delete_client_card'),
]
