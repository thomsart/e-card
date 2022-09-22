from django.shortcuts import render, redirect
from django.contrib.auth.models import User

from card.form import CardForm
from card.models import Card
from card.utils.tools import *



def add_card(requests, user_id):

    card_form = CardForm(requests.POST)

    if requests.method == 'GET':

        user = User.objects.get(id=user_id)

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

            user = User.objects.get(id=user_id)
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


def delete_card(requests, user_id, card_id):

    if requests.method == 'GET' and user_id and card_id:
        Card.objects.filter(id=card_id, user_id=user_id).delete()

        return redirect('clients')


context = {
    "mail": "psychoid@hotmail.fr",
    "first_name": "Thomas",
    "last_name": "Cottenceau"
}

def get_card(requests, user_id):

    if requests.method == 'GET':
        generate_QR_code(user_id)
        context['QR_code'] = download_QR_code(user_id)
        if context['QR_code']:
            print(context['QR_code'])
            email = send_email_new_card(context)

        if email:
            delete_QR_code(user_id)
            
            return redirect('clients')
