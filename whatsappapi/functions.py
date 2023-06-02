import datetime
import json
import os
from pathlib import Path

import requests
from googletrans import Translator

instructions = "📷 To help us analyze the leaf and identify any diseases accurately, please follow these steps when capturing and sending the photos:\n" \
               "🌞 Find a well-lit area for better visibility of the leaf, and make sure there are no shadows obscuring it.\n" \
               "🖐️ Place your hand behind the leaf to create a clear background and focus solely on the leaf itself.\n" \
               "📱 Hold your device steady while taking the photos to avoid any blurriness.\n" \
               "✨ Now, capture the photos following these steps:\n" \
               "1️⃣ Take a photo of the leaf from the top angle, showing its upper side.\n" \
               "2️⃣ Take another photo of the leaf from the top angle, ensuring a clear view of the upper side.\n" \
               "3️⃣ Capture a separate photo from the bottom angle, showcasing the lower side of the leaf.\n" \
               "📤 Once you have both photos, please send them as attachments to this chat.\n" \
               "🙏 Thank you for your cooperation! Well examine the photos and provide you with a diagnosis promptly."

def send_instructions(messenger, recipient_id, language):
    instructions = "Now  can send us photos of the leaf you want to identify. Please follow these steps when capturing and sending the photos:\n\n" \
                   "⚪ Find a well-lit area and avoid shadows on the leaf.\n" \
                   "⚪ Place your hand behind the leaf to focus only on it.\n" \
                   "⚪ Hold your device steady to avoid blurriness.\n" \
                   "⚪ take a photo from the top of the leaf.\n" \
                   "⚪ take another photo from the bottom of the leaf.\n" \
                   "⚪ Send both photos as attachments."
    translated_instructions = translate(instructions, language)
    messenger.send_message(
        recipient_id=recipient_id,
        message=translated_instructions,
    )


def get_name_plant(messenger, recipient_id):
    messenger.send_button(
        recipient_id=recipient_id,
        button={
            "header": "Choose name of plant",
            "body": "∎ please indicate the name of the plant you want to identify.",
            # "footer": "how much money he stil have",
            "action": {
                "button": "choose | اختر",
                "sections": [
                    {
                        "title": "language",
                        "rows": [
                            {"id": "list_plants-1", "title": "Tomato", "description": ""},
                            {"id": "list_plants-2", "title": "Potato", "description": ""},
                            {"id": "list_plants-3", "title": "Corn", "description": ""},
                            {"id": "list_plants-4", "title": "Strawberry", "description": ""},
                            {"id": "list_plants-5", "title": "Grape", "description": ""},
                            {"id": "list_plants-6", "title": "Apple", "description": ""},
                            {"id": "list_plants-7", "title": "Cherry", "description": ""},
                            {"id": "list_plants-8", "title": "Orrange", "description": ""},
                            {"id": "list_plants-9", "title": "Peach", "description": ""},
                            {"id": "list_plants-10", "title": "Bell Pepper", "description": ""},
                        ],
                    }
                ],
            },
        },

    )


def get_user_language(messenger, recipient_id):
    messenger.send_button(
        recipient_id=recipient_id,
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
                            {"id": "language-1", "title": "Arabic", "description": ""},
                            {"id": "language-2", "title": "Français", "description": ""},
                            {"id": "language-3", "title": "Anglais", "description": ""},
                        ],
                    }
                ],
            },
        },

    )

def translate(message, language):
    if language == "Français":
        language = "fr"
    elif language == "Anglais":
        language = "en"
    elif language == "Arabic":
        language = "ar"
    translator = Translator()
    translation = translator.translate(message ,dest=language)
    return translation.text
