import os

from django.core.mail import EmailMultiAlternatives
from django import template
import qrcode

from ecard.settings import BASE_DIR


def generate_pdf():
    pass

def generate_QR_code(context):

    try:
        img = qrcode.make(
            # voir comment on definis plus tard le path en fonction de l'OS
            "http://127.0.0.1:8000/" + "clients/" + context["user"]["id"] + "/card/" + context["card"]["id"],
            box_size=20
        )
        img.save(os.path.join("QR_codes", context["user"]["id"] + '_' + context["card"]["id"] + ".png"), 'PNG')
        return True

    except Exception:
        return False



def delete_QR_code(context):

    os.remove(os.path.join("QR_codes", context["user"]["id"] + '_' + context["card"]["id"] + ".png"))



def send_email_QR_code(context):
    """
    When a card is created, an e-mail is sending to the client with a QR code
    to retreive or share his new card.
    """

    if context:

        with open(os.path.join(BASE_DIR, "card", "templates", "email_card.html"), 'r') as temp:
            file = temp.read()
        file = file.replace("{{ context.card.profession }}", context["card"]["profession"])
        # render email text

        email_plaintext_message = template.loader.get_template('email_card.txt').render(context)

        msg = EmailMultiAlternatives(
            # title:
            "Bonjour " + context["user"]["first_name"] + " " + context["user"]["last_name"] + " !",
            # message:
            email_plaintext_message,
            # from:
            "psychoid77@gmail.com",
            # to:
            [context["user"]["email"]]
        )

        msg.attach_alternative(file, "text/html")
        msg.attach_file(os.path.join("QR_codes", context["user"]["id"] + '_' + context["card"]["id"] + ".png"))
        msg.send()

        return True