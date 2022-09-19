from django.shortcuts import render

from django.contrib.auth.models import User
from card.models import Card

# render(request, 'home.html', context)
# return redirect('selected_product/', product_id=product_id)


def clients(requests):

    if requests.method == 'GET':

        clients = User.objects.all().values()
        for client in clients:
            print(client)
        context = {
            'clients': clients
        }

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