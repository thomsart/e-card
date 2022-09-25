from django.shortcuts import render, redirect
from django.contrib.auth.models import User

from card.form import CardForm
from card.models import Card
from card.utils.tools import *



def add_card(requests, user_id):

    card_form = CardForm(requests.POST)
    user = User.objects.get(id=user_id)

    if requests.method == 'GET':

        return render(
            requests,
            'add_card.html',
            {
                'user_id': user_id,
                'user_first_name': user.first_name,
                'user_last_name': user.last_name,
                'user_email': user.email,
                'CardForm': card_form
            }
        )

    if requests.method == 'POST':
        if card_form.is_valid():
            
            Card.objects.create(
                profession=card_form.cleaned_data['profession'],
                phone=card_form.cleaned_data['phone'],
                email=card_form.cleaned_data['email'],
                user=user
            )

            return redirect('clients')

        else:
            print("Card not created")

            return redirect('add_card', user_id)



def get_card(requests, user_id, card_id):
    pass



def delete_card(requests, user_id, card_id):

    if requests.method == 'GET' and user_id and card_id:
        Card.objects.filter(id=card_id, user_id=user_id).delete()

        return redirect('clients')



def send_email_link(requests, user_id, card_id):

    user = User.objects.get(id=user_id)
    card = Card.objects.get(id=card_id)

    if user and card:
        if requests.method == 'GET':
            generate_QR_code(user_id, card_id)
            email = send_email_QR_code(user_id, card_id)

            if email:
                delete_QR_code(user_id, card_id)

                return redirect('clients')

        else:
            print("Email not send")
    
    else:
        print("Unknown CLient")
