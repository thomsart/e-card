import os

from django.core.mail import EmailMultiAlternatives
from django import template
import qrcode
from fpdf import FPDF

from ecard.settings import BASE_DIR, MEDIA_ROOT, ALLOWED_HOSTS



def formate_text(text: str):

    # split_text = text.split(" ")
    # final_text = ""
    # count = 0
    # for word in split_text:
    #     final_text = final_text + " "
    #     count += 1
    #     for char in word:
    #         count += 1
    #         if count > 49:
    #             while final_text[-1] != " ":
    #                final_text = final_text[:-1]
    #             final_text = final_text + "|" + word
    #             count = 0
    #             break
    #         else:
    #             final_text = final_text + char

    return '"' + text + '"'



# def generate_pdf(context):

#     mon_pdf = FPDF()
#     mon_pdf.add_page()
#     mon_pdf.set_margins(left=20.0, right=20.0, top=50)
#     mon_pdf.set_font("Arial", size=40)
#     # each cell represente a square in wich we put text or photo
#     mon_pdf.ln(h=10)
#     mon_pdf.ln(h=10)
#     mon_pdf.cell(0, 10, txt=context["name"], ln=1, align='L') #, border=1
#     mon_pdf.ln(h=10)
#     mon_pdf.cell(0, 10, txt=context["profession"], ln=1)
#     mon_pdf.ln(h=10)

#     # image
#     mon_pdf.image("PDFs/photo_chen.jpg" , x=None, y=None, w=50, h=80, type='JPG')
#     mon_pdf.ln(h=10)

#     # description text
#     mon_pdf.set_font("Arial", size=20)
#     text = context["description"].split("|")
#     for part in text:
#         mon_pdf.cell(0, 10, txt=part, ln=1)

#     mon_pdf.ln(h=30)

#     # links
#     phone = context["phone"]
#     mon_pdf.set_font("Arial", size=40)
#     mon_pdf.add_link()
#     mon_pdf.ln(h=10)
#     mon_pdf.link(x=0, y=150, w=80, h=10, link=context["email"])
#     mon_pdf.ln(h=10)
#     mon_pdf.write(10, context["email"], link="https://www.thomsart.tech")
#     mon_pdf.ln(h=10)

#     mon_pdf.output(MEDIA_URL + context['pdf_name'] + ".pdf")

#     return mon_pdf

# def delete_pdf():
#     pass



def generate_QR_code(context):

    try:
        img = qrcode.make(
            ALLOWED_HOSTS[0] + "/clients/" + context["user"]["id"] + "/card/" + context["card"]["id"],
            box_size=20
        )
        img.save(os.path.join(MEDIA_ROOT, context["user"]["id"] + '_' + context["card"]["id"] + ".png"), 'PNG')

        return True

    except Exception:

        return False



def delete_QR_code(context):

    os.remove(os.path.join(MEDIA_ROOT, context["user"]["id"] + '_' + context["card"]["id"] + ".png"))



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
        msg.attach_file(os.path.join(MEDIA_ROOT, context["user"]["id"] + '_' + context["card"]["id"] + ".png"))
        msg.send()

        return True