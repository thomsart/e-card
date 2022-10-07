from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from account.form import ClientForm, LoginForm
from card.models import Card



def user_login(requests):

    login_form = LoginForm(requests.POST)

    if requests.method == 'GET':

        return render(requests, 'login.html', {'login_form': LoginForm})

    if requests.method == 'POST':
        if login_form.is_valid():
            connection = authenticate(
                username=login_form.cleaned_data["email"], password=login_form.cleaned_data["password"]
            )

            if connection:
                login(requests, connection)

                return redirect('clients')

            else:
                print("Connexion failled")


def user_logout(requests):

    logout(requests)

    return redirect("user_login")


@login_required
def user_register(requests):
    return redirect('user_login')


@login_required
def clients(requests):

    if requests.method == 'GET':

        context = {"user_cards": []}
        users = User.objects.filter(is_superuser=False, is_staff=False).all().order_by('-date_joined')

        for user in users:
            couple = {}
            couple['user'] = user
            couple['cards'] = Card.objects.filter(user_id=user.id)
            context['user_cards'].append(couple)

        return render(requests, 'clients.html', context)

    else:
        redirect('login')


@login_required
def add_client(requests):

    client_form = ClientForm(requests.POST)

    if requests.method == 'GET':

        return render(requests, 'client_form.html', {'ClientForm': client_form})

    if requests.method == 'POST':
        if client_form.is_valid():

            User.objects.create(
                first_name=client_form.cleaned_data['first_name'].capitalize(),
                last_name=client_form.cleaned_data['last_name'].capitalize(),
                email=client_form.cleaned_data['email'],
                username=client_form.cleaned_data['email'],
                password='1234+' + client_form.cleaned_data['email'] + '-4321'
            )

            return redirect('clients')

        else:

            return redirect('add_client')


@login_required
def desactivate_reactivate_client(requests, user_id):

    if requests.method == 'GET' and user_id:
        user = User.objects.get(id=user_id)
        print(user)
        print(type(user))
        if user.is_active == True:
            User.objects.filter(id=user_id).update(is_active=False)
        else:
            User.objects.filter(id=user_id).update(is_active=True)

        return redirect('clients')


@login_required
def delete_client(requests, user_id):

    if requests.method == 'GET' and user_id:
        User.objects.filter(id=user_id).delete()

        return redirect('clients')
