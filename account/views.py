from django.shortcuts import render, redirect
from django.contrib.auth.models import User

from account.form import ClientForm
from card.models import Card



def clients(requests):

    if requests.method == 'GET':
        context = {'user_cards': []}
        users = User.objects.all().order_by('-date_joined')
        for user in users:
            couple = {}
            couple['user'] = user
            couple['cards'] = Card.objects.filter(user_id=user.id)
            context['user_cards'].append(couple)

        return render(requests, 'clients.html', context)


def add_client(requests):

    client_form = ClientForm(requests.POST)

    if requests.method == 'GET':

        return render(requests, 'client_form.html', {'ClientForm': client_form})

    if requests.method == 'POST':
        if client_form.is_valid():
            
            User.objects.create(
                first_name=client_form.cleaned_data['first_name'],
                last_name=client_form.cleaned_data['last_name'],
                email=client_form.cleaned_data['email'],
                username=client_form.cleaned_data['email'],
                password='1234+'+str(client_form.cleaned_data['email'])+'-4321'
            )

            return redirect('clients')
        else:
            return redirect('add_client')


def delete_client(requests, user_id):

    if requests.method == 'GET' and user_id:
        User.objects.filter(id=user_id).delete()

        return redirect('clients')
