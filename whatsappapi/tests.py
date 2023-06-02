from googletrans import Translator

# function that takes a message and translates it

def translate(message):
    translator = Translator()
    translation = translator.translate(message ,dest='francais')
    return translation.text
# Add the message handler to the bot


message = "1- Find a well-lit area and avoid shadows on the leaf.\n" \
          "2- Place your hand behind the leaf to focus only on it.\n" \
          "3- Hold your device steady to avoid blurriness.\n " \
          "4- Capture a photo from the top of the leaf\n" \
          "5- Capture another photo from the bottom of the leaf\n" \
          "6- Send both photos as attachments."

translated_message = translate(message)
print(translated_message)

