import os

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password, check_password

from django.contrib.auth.models import User, Group
from django.http import HttpResponse

from ecard.settings import MEDIA_ROOT
from account.form import ClientForm, LoginForm
from card.models import Card



def user_login(requests):

    login_form = LoginForm(requests.POST)

    if requests.method == 'GET':

        return render(requests, 'login.html', {'login_form': LoginForm})

    if requests.method == 'POST':
        if login_form.is_valid():
            user = authenticate(
                username=login_form.cleaned_data["email"],
                password=login_form.cleaned_data["password"]
            )
            if user:
                login(requests, user)

                return redirect('home')

            else:
                return HttpResponse("Access refused")

        else:
            return HttpResponse("Error in form")


def user_logout(requests):

    logout(requests)

    return redirect("user_login")


@login_required
def user_register(requests):
    return redirect('user_login')


@login_required
def home(requests):

    if requests.method == 'GET':

        user_loged_in = User.objects.get(id=requests.user.id)
        if user_loged_in.is_superuser:
            users = User.objects.filter(is_superuser=False, is_staff=False).all().order_by('-date_joined')
        else:
            group = Group.objects.get(user=user_loged_in)
            users = User.objects.filter(is_superuser=False, is_staff=False, groups=group).all().order_by('-date_joined')
        context = {"user_loged_in": user_loged_in, "user_cards": []}

        if len(users) != 0:
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
            user_loged_in = User.objects.get(id=requests.user.id)
            group = Group.objects.get(user=user_loged_in)

            new_user = User.objects.create(
                first_name=client_form.cleaned_data['first_name'].capitalize(),
                last_name=client_form.cleaned_data['last_name'].capitalize(),
                email=client_form.cleaned_data['email'],
                username=client_form.cleaned_data['email'],
                password=make_password(
                    '1234+' + client_form.cleaned_data['email'] + '-4321',
                    salt=None,
                    hasher='default')
            )
            group.user_set.add(new_user)

            return redirect('home')

        else:

            return redirect('add_client')


@login_required
def deactivate_reactivate_client(requests, user_id):

    user = User.objects.get(id=user_id)

    if requests.method == 'GET' and user:

        if user.is_active == True:
            User.objects.filter(id=user.id).update(is_active=False)
        else:
            User.objects.filter(id=user.id).update(is_active=True)

        return redirect('home')


@login_required
def delete_client(requests, user_id):

    client = User.objects.get(id=user_id)

    if requests.method == "GET" and client:

        return render(requests, "client_delete.html", {"user": client})

    elif requests.method == "POST" and client:

        # we decide to delete all photos of these user's cards in the uploads first
        list_of_card_to_delete = [card.photo for card in Card.objects.filter(user_id=client.id)]
        for card in list_of_card_to_delete:
            os.remove(os.path.join(MEDIA_ROOT, str(card)))
        client.delete()

        return redirect('home')
