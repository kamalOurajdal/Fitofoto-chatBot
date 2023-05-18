import datetime
import json
import os
import environ
from django.http import HttpResponse
import uuid
import warnings
import logging
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from heyoo import WhatsApp

from detectionapi.functions import detect_image
from weatherapi.weatherapi import get_weather_data
from azuregpt.azureopenai import sendgpt
from .functions import get_user_language

from .models import TextMessage, Conversation, LocationMessage, ImageMessage, VideoMessage, AudioMessage, \
    DocumentMessage

from farmers.models import Farmer


warnings.filterwarnings("ignore")

from django.shortcuts import render

# Create your views here.




env = environ.Env()
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))


messenger = WhatsApp(token=env('WHATSAPP_TOKEN'), phone_number_id=env('PHONE_NUMBER_ID'))
@csrf_exempt
@require_http_methods(['GET'])
def verify_token(request):
    logging.info("trying to verify webhook")
    if request.GET.get('hub.verify_token') == env('VERIFY_TOKEN'):
        logging.info("verified webhook")
        challenge = request.GET.get('hub.challenge')

        return HttpResponse(challenge, "text/plain", status=200)
    else:
        logging.error("webhook verification failed")
        return HttpResponse("invalide verification token", status=400)

@csrf_exempt
def whatsapp_webhook(request):
    if request.method == 'POST':

        data = json.loads(request.body)

        changed_field = messenger.changed_field(data)
        if changed_field == "messages":
            new_message = messenger.get_mobile(data)
            if new_message:
                mobile = messenger.get_mobile(data)
                name = messenger.get_name(data)
                logging.info("a new message has been received from {}".format(mobile))

                #check if the conversation already exists
                if not Conversation.objects.filter(phone_number=mobile).exists():
                    Conversation.objects.create(phone_number=mobile, name=name, )
                    logging.info("new conversation")
                    new_conversation = True
                else:
                    new_conversation = False
                    logging.info("existing conversation")

                #check if the farmer is subscribed
                if Farmer.objects.filter(phone_number=mobile).exists():
                    farmer = Farmer.objects.get(phone_number=mobile)
                    if farmer.is_subsribed:
                        logging.info("farmer is subscribed")
                        allow_acces = True
                    else:
                        logging.info("farmer is not subscribed")
                        allow_acces = False

                message_type = messenger.get_message_type(data)

                conversation = Conversation.objects.get(phone_number=mobile)
                # check if the message is a text message
                if message_type == "text":
                    message = messenger.get_message(data)
                    TextMessage.objects.create(
                        conversation= conversation,
                        message=message,)
                    logging.info("text message saved")

                    #check if is a new conversation with the user
                    if new_conversation:
                        # send message to gpt
                        gpt = sendgpt(str(datetime.datetime.now()) + message)
                        # send a reply to the user
                        messenger.send_message(gpt, mobile)
                        #save the reply to the database
                        TextMessage.objects.create(
                            conversation = conversation,
                            message = gpt,
                            sent_by_bot = True,)

                        get_user_language(messenger, mobile)



                    # check if the message is an upgrade message
                    elif message.lower() == "upgrade":
                        if not allow_acces:
                            messenger.send_message(
                                message = "You are seccessfully upgraded your account, "
                                "you can now send voice messges and generate reports",
                                recipient_id = mobile )
                            TextMessage.objects.create(
                                conversation = conversation,
                                message = "You are seccessfully upgraded your account, "
                                "you can now send voice messges and generate reports",
                                sent_by_bot = True,
                            )
                            farmer.is_subsribed = True
                            farmer.save()
                        else:
                            messenger.send_message(
                                message = "You are already upgraded your account. ",
                                recipient_id = mobile )
                            TextMessage.objects.create(
                                conversation = conversation,
                                message = "You are already upgraded your account.",
                                sent_by_bot = True,)
                    # GPT will reply to the user
                    else:
                        #resond to the user in the same language
                        gpt = sendgpt(str(datetime.datetime.now()) + f', user: respond to this message in {conversation.conversation_language} '+ message)
                        # send a reply to the user
                        messenger.send_message(gpt, mobile)

                elif message_type == "interactive":
                    message_response = messenger.get_interactive_response(data)
                    interactive_type = message_response.get("type")
                    message_text = message_response[interactive_type]["title"]
                    logging.info(f"Your selected language is : {message_text}")
                    conversation.conversation_language = message_text
                    conversation.save()

                elif message_type == "location":
                    message_location = messenger.get_location(data)
                    message_latitude = message_location["latitude"]
                    message_longitude = message_location["longitude"]

                    # save the location to the database
                    LocationMessage.objects.create(
                        conversation=Conversation.objects.get(phone_number=mobile),
                        latitude=message_latitude,
                        longitude=message_longitude,
                    )
                    weather_data = get_weather_data(message_latitude, message_longitude)

                    weather_main = weather_data["weather"][0]["main"]
                    wind_speed = weather_data["wind"]["speed"]
                    pressure = weather_data["main"]["pressure"]
                    city_name = weather_data["name"]
                    temperature = weather_data["main"]["temp"]-273.15
                    humidity = weather_data["main"]["humidity"]
                    weather_description = weather_data["weather"][0]["description"]

                    answer = sendgpt(f"respond to this message in {conversation.conversation_language} weather:{weather_main}_{temperature}C_location:{city_name}")
                    messenger.send_message(answer, mobile)
                    logging.info("Location: %s, %s", message_latitude, message_longitude)


                elif message_type == "image":
                    image = messenger.get_image(data)
                    image_id, mime_type = image["id"], image["mime_type"]
                    image_url = messenger.query_media_url(image_id)
                    unique_name = str(uuid.uuid1())
                    # save the file to the server and get the file location
                    image_filename = messenger.download_media(image_url, mime_type, f"files/images/{unique_name}")

                    # save the image location to the database
                    ImageMessage.objects.create(
                        conversation=Conversation.objects.get(phone_number=mobile),
                        image_message=image_filename,
                    )
                    pred_class, confidence = detect_image(image_filename)
                    solution_gpt = sendgpt(f"respond to this message in {conversation.conversation_language}plant_leaf_disease_detected:{pred_class}")
                    messenger.send_message(solution_gpt, mobile)
                    print(f"{mobile} sent image {image_filename}")
                    logging.info(f"{mobile} sent image {image_filename}")


                elif message_type == "video":
                    video = messenger.get_video(data)
                    video_id, mime_type = video["id"], video["mime_type"]
                    video_url = messenger.query_media_url(video_id)
                    unique_name = str(uuid.uuid1())
                    video_filename = messenger.download_media(video_url, mime_type, f"files/videos/{unique_name}")

                    # save the video location to the database
                    VideoMessage.objects.create(
                        conversation=Conversation.objects.get(phone_number=mobile),
                        video_message=video_filename,
                    )
                    print(f"{mobile} sent video {video_filename}")
                    logging.info(f"{mobile} sent video {video_filename}")


                elif message_type == "audio":
                    audio = messenger.get_audio(data)
                    audio_id, mime_type = audio["id"], audio["mime_type"]
                    audio_url = messenger.query_media_url(audio_id)
                    unique_name = str(uuid.uuid1())
                    # save the file to the server and get the file location
                    audio_filename = messenger.download_media(audio_url, mime_type, f"files/audios/{unique_name}")

                    # save the audio location to the database
                    AudioMessage.objects.create(
                        conversation=Conversation.objects.get(phone_number=mobile),
                        audio_message=audio_filename,
                    )
                    messenger.send_audio(
                        audio="files/audios/test.mp3",
                        recipient_id=mobile,
                    )
                    print(f"{mobile} sent audio {audio_filename}")
                    logging.info(f"{mobile} sent audio {audio_filename}")


                elif message_type == "document":
                    file = messenger.get_document(data)
                    file_id, mime_type = file["id"], file["mime_type"]
                    file_url = messenger.query_media_url(file_id)
                    unique_name = str(uuid.uuid1())
                    #save the file to the server and get the file location
                    file_filename = messenger.download_media(file_url, mime_type, f"files/documents/{unique_name}")

                    # save the file to the database
                    DocumentMessage.objects.create(
                        conversation=Conversation.objects.get(phone_number=mobile),
                        document_message=file_filename,
                    )
                    print(f"{mobile} sent file {file_filename}")
                    logging.info(f"{mobile} sent file {file_filename}")

                else:
                    print(f"{mobile} sent {message_type} ")
                    print(data)

            # check if the message was dilivered
            else:
                delivery = messenger.get_delivery(data)
                if delivery:
                    print(f"Message : {delivery}")
                else:
                    print("No new message")

        return HttpResponse(status=200)

    else:
        return HttpResponse(status=405)

def index(request):
    return HttpResponse("Welocom to fitofoto")










