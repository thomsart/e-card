import os

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password

from django.contrib.auth.models import User, Group
from django.http import HttpResponse

from ecard.settings import MEDIA_ROOT
from account.form import ClientForm, LoginForm
from card.models import Card
from account.models import Phone



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
def home(requests):

    if requests.method == 'GET':

        context = {
            "user" : User.objects.get(id=requests.user.id),
            "phone": Phone.objects.get(user_id=requests.user.id),
            "cards": Card.objects.filter(user_id=requests.user.id),
            "groups": []
        }

        if context["user"].is_staff and context["user"].is_active:
            groups = Group.objects.filter(user=context["user"])
            for group in groups:
                data = {group.name: []}
                clients = User.objects.filter(
                    is_superuser=False,
                    is_staff=False,
                    groups=group
                ).all().order_by('-date_joined')
                if len(clients) != 0:  
                    for client in clients:
                        couple = {}
                        couple["user"] = client
                        couple["phone"] = Phone.objects.get(user_id=client.id)
                        cards = Card.objects.filter(user_id=client.id)
                        if cards:
                            couple["cards"] = cards
                        data[group.name].append(couple)
                context["groups"].append(data)
            # print(context)

        return render(requests, 'clients.html', context)

    else:

        return redirect('login')


@login_required
def add_client(requests, group):

    client_form = ClientForm(requests.POST)

    if requests.method == 'GET':

        return render(requests, 'client_form.html', {'ClientForm': client_form, "group": group})

    if requests.method == 'POST':
        if client_form.is_valid():

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

            in_group = Group.objects.get(name=group)
            in_group.user_set.add(new_user)
            Phone.objects.create(number=client_form.cleaned_data['phone'], user_id=new_user.id)

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
