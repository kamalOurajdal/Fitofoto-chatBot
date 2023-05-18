import os
import environ
from django.test import TestCase
from heyoo import WhatsApp

# Create your tests here.
env = environ.Env()
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))
verify_token = str(env('VERIFY_TOKEN'))
whatsapp_token = str(env('WHATSAPP_TOKEN'))
phone_number_id = str(env('PHONE_NUMBER_ID'))

print("verify_token:", verify_token)


messenger = WhatsApp(token=whatsapp_token, phone_number_id=phone_number_id)

# messenger.send_reply_button(
#         recipient_id="212607715898",
#         button={
#             "type": "button",
#             "body": {
#                 "text": "This is a test button"
#             },
#             "action": {
#                 "buttons": [
#                     {
#                         "type": "reply",
#                         "reply": {
#                             "id": "b1",
#                             "title": "This is button 1"
#                         }
#                     },
#                     {
#                         "type": "reply",
#                         "reply": {
#                             "id": "b2",
#                             "title": "this is button 2"
#                         }
#                     }
#                 ]
#             }
#       },
#     )


messenger.send_button(
    recipient_id="212607715898",
    button={
        "header": "Choose your language | اختر لغتك",
        "body": "∎ In order to better assist you, please indicate the language you prefer to use for communication."
                " \n\n ∎ من أجل مساعدتك بشكل أفضل ، يرجى تحديد اللغة التي تفضل استخدامها للتواصل.",
        # "footer": "how much money he stil have",
        "action": {
            "button": "choose | اختر",
            "sections": [
                {
                    "title": "language",
                    "rows": [
                        {"id": "row 1", "title": "Arabic", "description": ""},
                        {"id": "row 2", "title": "Français", "description": ""},
                        {"id": "row 3", "title": "Anglais", "description": ""},
                    ],
                }
            ],
        },
    },

)