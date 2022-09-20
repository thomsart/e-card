from django.shortcuts import render

from django.contrib.auth.models import User
from card.models import Card

# render(request, 'home.html', context)
# return redirect('selected_product/', product_id=product_id)


def clients(requests):

    if requests.method == 'GET':
        context = {'user_cards': []}
        users = User.objects.all()
        for user in users:
            couple = {}
            couple['user'] = user
            couple['cards'] = Card.objects.filter(user_id=user.id)
            context['user_cards'].append(couple)

        return render(requests, 'clients.html', context)


def add_client(requests):
    pass


def add_card(requests):
    pass


def delete_card(requests):
    pass


def delete_client(requests):
    pass





def get_card(requests, user_id):
    pass