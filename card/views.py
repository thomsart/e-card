from django.shortcuts import render, redirect
from django.contrib.auth.models import User

from card.form import CardForm
from card.models import Card
from card.utils.tools import *



def add_card(requests, user_id):

    user = User.objects.get(id=user_id)
    card_form = CardForm(requests.POST, requests.FILES)

    if requests.method == 'GET':
        return render(
            requests,
            'card_form.html',
            {
                'user_id': str(user.id),
                'user_first_name': user.first_name,
                'user_last_name': user.last_name,
                'user_email': user.email,
                'CardForm': card_form
            }
        )

    if requests.method == 'POST':
        if card_form.is_valid():
            # print(requests.POST)
            # print(requests.FILES)
            if card_form["description"] != "":
                card_form.cleaned_data["description"] = formate_text(card_form.cleaned_data["description"])

            Card.objects.create(
                profession=card_form.cleaned_data['profession'].capitalize(),
                phone=card_form.cleaned_data['phone'],
                email=card_form.cleaned_data['email'],
                description=card_form.cleaned_data['description'],
                photo=card_form.cleaned_data['photo'],
                user=user
            )
            return redirect('clients')

        else:
            print("Card not created")

            return redirect('add_card', user_id)



def get_card(requests, user_id, card_id):

    user = User.objects.get(id=user_id)
    card = Card.objects.get(id=card_id)

    if requests.method == 'GET' and user and card:
 
        return render(requests, "card.html", {
            "couple": {"user": user},
            "card": card
            }
        )

    else:
        return print("This Client or Card doesn't exist !")



def delete_card(requests, user_id, card_id):

    if requests.method == 'GET' and user_id and card_id:
        Card.objects.filter(id=card_id, user_id=user_id).delete()

        return redirect('clients')



def send_email_link(requests, user_id, card_id):

    user = User.objects.get(id=user_id)
    card = Card.objects.get(id=card_id)

    context = {
        "user": {
            "id": str(user.id),
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
        },
        "card": {
            "id": str(card.id),
            "profession": card.profession
        }
    }

    if context:
        if requests.method == 'GET':
            if generate_QR_code(context):   
                send_email_QR_code(context)
                delete_QR_code(context)

                return redirect('clients')

        else:
            print("Email not send")
    else:
        print("Unknown CLient")
