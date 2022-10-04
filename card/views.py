# import os
from django.shortcuts import render, redirect
from django.template.loader import get_template, render_to_string
from django.conf import settings
from django.contrib.staticfiles import finders
from django.http import HttpResponse
from django.contrib.auth.models import User

from xhtml2pdf import pisa

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
                email=user.email,
                description=card_form.cleaned_data['description'],
                photo=card_form.cleaned_data['photo'],
                user=user
            )
            return redirect('clients')

        else:
            print("Card not created")

            return redirect('add_card', user_id)



# def get_card(requests, user_id, card_id):

#     user = User.objects.get(id=user_id)
#     card = Card.objects.get(id=card_id)

#     if requests.method == 'GET' and user.is_active and card:
#         # html = get_template("card.html")
#         # html = get_template("card.html", request=None, context={"couple": {"user": user}, "card": card})
#         # html = template.loader.get_template("card.html").render({"couple": {"user": user}, "card": card})
#         html = "<html><body><p>To PDF or not to PDF</p></body></html>"
#         pdf = generate_pdf(user_id + "_" + card_id)

#         print(html)
#         print(type(html))

#         if html and pdf:
#             return convert_html_to_pdf(html, pdf)

#     else:
#         return print("This Client or Card doesn't exist !")



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
        sUrl = settings.STATIC_URL        # Typically /static/
        sRoot = settings.STATIC_ROOT      # Typically /home/userX/project_static/
        mUrl = settings.MEDIA_URL         # Typically /uploads/
        mRoot = settings.MEDIA_ROOT       # Typically /home/userX/project_static/uploads/

        if uri.startswith(mUrl):
            path = os.path.join(mRoot, uri.replace(mUrl, ""))
        elif uri.startswith(sUrl):
            path = os.path.join(sRoot, uri.replace(sUrl, ""))
        else:
            return uri

    # make sure that file exists
    if not os.path.isfile(path):
        raise Exception('media URI must start with %s or %s' % (sUrl, mUrl))

    return path



def get_card(requests, user_id, card_id):

    user = User.objects.get(id=user_id)
    card = Card.objects.get(id=card_id)
    context = {"couple": {"user": user}, "card": card}

    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=' + card.profession + '_' +  user.first_name + '_' + user.last_name
    # find the template and render it.
    template = get_template("pdf_card.html")
    html = template.render(context)
    # create a pdf
    pisa_status = pisa.CreatePDF(html, link_callback=link_callback, dest=response)
    # if error then show some funny view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')

    return response



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
