from django.shortcuts import render, redirect
from django.contrib.auth.models import User

from account.form import UserForm
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

    form = UserForm(requests.POST)

    if requests.method == 'GET':
        return render(requests, 'add_client.html', {'UserForm': form})

    if requests.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('clients')


def add_card(requests):

    if requests.method == 'GET':
        return redirect('clients')


def delete_card(requests):

    if requests.method == 'GET':
        return redirect('clients')


def delete_client(requests):

    if requests.method == 'GET':
        return redirect('clients')





def get_card(requests, user_id):
    pass