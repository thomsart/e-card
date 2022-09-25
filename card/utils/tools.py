import os

from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django import template
import qrcode

from ecard.settings import BASE_DIR
from card.models import Card



def generate_QR_code(user_id, card_id):

    try:
        img = qrcode.make("http://127.0.0.1:8000/" + "clients/" + user_id + "/card/" + card_id, box_size=20)
        img.save(os.path.join("QR_codes", str(user_id) + '_' + str(card_id) + ".png"), 'PNG')
        return True

    except Exception:
        return False



def delete_QR_code(user_id, card_id):

    os.remove(os.path.join("QR_codes", str(user_id) + '_' + str(card_id) + ".png"))



def send_email_QR_code(user_id, card_id):
    """
    When a card is created, an e-mail is send to the client with a QR code
    to retreive his new card.
    """

    user = User.objects.get(id=user_id)
    card = Card.objects.get(id=card_id)

    if user and card:

        with open(os.path.join(BASE_DIR, "card", "templates", "new_card.html"), 'r') as temp:
            file = temp.read()
        # render email text
        context = {
            "user_first_name": user.first_name,
            "user_last_name": user.last_name,
        }
        email_plaintext_message = template.loader.get_template('new_card.txt').render(context)

        msg = EmailMultiAlternatives(
            # title:
            "Bonjour " + str(user.first_name) + " " + str(user.last_name) + " !",
            # message:
            email_plaintext_message,
            # from:
            "psychoid77@gmail.com",
            # to:
            ["psychoid@hotmail.fr",
            "psychoid77@gmail.com"]
        )

        msg.attach_alternative(file, "text/html")
        msg.attach_file(os.path.join("QR_codes", str(user_id) + '_' + str(card_id) + ".png"))
        msg.send()

        return True