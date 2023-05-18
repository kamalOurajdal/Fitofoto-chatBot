import datetime
import json
import os
from pathlib import Path

import requests


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
                            {"id": "row 1", "title": "Arabic", "description": ""},
                            {"id": "row 2", "title": "Français", "description": ""},
                            {"id": "row 3", "title": "Anglais", "description": ""},
                        ],
                    }
                ],
            },
        },

    )