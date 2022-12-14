from django.shortcuts import render, redirect
from django.template.loader import get_template
from django.conf import settings
from django.contrib.staticfiles import finders
from django.http import HttpResponse
from django.contrib.auth.models import User

from xhtml2pdf import pisa

from card.form import CardForm
from card.models import Card
from account.models import Phone
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

    if requests.method == 'POST' and user.is_active:
        if card_form.is_valid():
            # print(requests.FILES)

            if card_form.cleaned_data["title"] != "":
                card_form.cleaned_data['title'].capitalize()
            else:
                card_form.cleaned_data['title'] = "Virtual-Card"

            if card_form.cleaned_data["description"] != "":
                card_form.cleaned_data["description"] = '" ' + card_form.cleaned_data["description"] + ' "'

            Card.objects.create(
                title=card_form.cleaned_data['title'],
                photo=card_form.cleaned_data['photo'],
                description=card_form.cleaned_data["description"],
                website=card_form.cleaned_data['website'],
                user=user
            )
            return redirect('home')

        else:

            return redirect('add_card', user_id)



def link_callback(uri, rel):
    """
    Convert HTML URIs to absolute system paths so xhtml2pdf can access those
    resources.
    """

    result = finders.find(uri)

    if result:
        if not isinstance(result, (list, tuple)):
            result = [result]
        result = list(os.path.realpath(path) for path in result)
        path=result[0]
    else:
        static_url = settings.STATIC_URL
        static_root = settings.STATIC_ROOT
        media_url = settings.MEDIA_URL
        media_root = settings.MEDIA_ROOT

        if uri.startswith(media_url):
            path = os.path.join(media_root, uri.replace(media_url, ""))
        elif uri.startswith(static_url):
            path = os.path.join(static_root, uri.replace(static_url, ""))
        else:
            return uri

    # make sure that file exists
    if not os.path.isfile(path):
        raise Exception('media URI must start with %s or %s' % (static_url, media_url))

    return path



def get_card(requests, user_id, user_email, card_id):

    user = User.objects.get(id=user_id)
    card = Card.objects.get(id=card_id)
    phone = Phone.objects.get(user_id=user.id)

    if requests.method == "GET" and user.is_active and card and check_email(user.email, user_email):

        context = {
            "title": card.title,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "photo": card.photo,
            "description": card.description,
            "website": card.website,
            "email": user.email,
            "phone": phone.number,
        }

        # Create a Django response object, and specify content_type as pdf
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename=' + card.title + '_' +  user.first_name + '_' + user.last_name
        # find the template and render it.
        template = get_template("pdf_card.html")
        html = template.render(context)
        # create a pdf
        pisa_status = pisa.CreatePDF(html, link_callback=link_callback, dest=response)
        # if error then show some funny view
        if pisa_status.err:
            return HttpResponse('We had some errors <pre>' + html + '</pre>')

        return response

    else:

        return HttpResponse("No access to this card")



def delete_card(requests, user_id, card_id):

    if requests.method == 'GET' and user_id and card_id:
        card = Card.objects.get(id=card_id, user_id=user_id)
        if card.photo:
            os.remove(os.path.join(settings.MEDIA_ROOT, str(card.photo)))
        card.delete()

        return redirect('home')



def send_email_link(requests, user_id, card_id):

    user = User.objects.get(id=user_id)
    card = Card.objects.get(id=card_id)

    if requests.method == 'GET' and user.is_active and card:

        context = {
            "user": {
                "id": str(user.id),
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
            },
            "card": {
                "id": str(card.id),
                "title": card.title
            }
        }

        if generate_QR_code(context):   
            if send_email_QR_code(context):
                delete_QR_code(context)

                return redirect('home')

            else:
                delete_QR_code(context)

                return HttpResponse("Email not send, is the address email correct ?")

        else:
            return HttpResponse("Problem to generate a QR code.")

    else:
        return HttpResponse("Unknown or deactivated client. Or the card doesn't exists anymore.")
