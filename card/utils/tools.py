import os
from ecard.settings import BASE_DIR

from django.core.mail import EmailMultiAlternatives
from django import template
import qrcode
import qrcode.image.svg



def generate_QR_code(user_id):

    try:
        img = qrcode.make("http://www.thomsart.tech", box_size=10)
        img.save('QR_codes/' + str(user_id) + '.png', 'PNG')
        return True

    except Exception:
        return False


def download_QR_code(user_id):

    QR_code = open("QR_codes/" + user_id + ".png", 'r')

    return QR_code


def delete_QR_code(user_id):
    pass


def send_email_new_card(context):
    """
    When a card is created, an e-mail is send to the client with a QR code
    to retreive his new card.
    """

    path = os.path.join(BASE_DIR, "card", "templates", "new_card.html")
    with open(path, 'r') as temp:
        file = temp.read()

    file_trans = file.replace('{{ first_name }}', context['first_name'])
    file_trans = file.replace('{{ last_name }}', context['last_name'])

    # render email text
    email_plaintext_message = template.loader.get_template('new_card.txt').render(context)

    msg = EmailMultiAlternatives(
        # title:
        "Votre QR-code pour generer votre carte de visite.",
        # message:
        email_plaintext_message,
        # from:
        "psychoid77@gmail.com",
        # to:
        [context['mail']]
    )

    msg.attach_alternative(file_trans, "text/html")
    msg.send()

    return True