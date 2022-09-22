import os
from ecard.settings import BASE_DIR

from django.core.mail import EmailMultiAlternatives
from django import template



def send_email_new_client(context):
    """
    When a Client is created, an e-mail is send to him.
    """

    path = os.path.join(BASE_DIR, "account", "templates", "new_client.html")
    with open(path, 'r') as temp:
        file = temp.read()

    file_trans = file.replace('{{ first_name }}', context['first_name'])
    file_trans = file.replace('{{ last_name }}', context['last_name'])

    # render email text
    email_plaintext_message = template.loader.get_template('new_client.txt').render(context)

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