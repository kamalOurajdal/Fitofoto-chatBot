from django.shortcuts import render

# Create your views here.
def sendgpt(message):
    return "this is a reply to " + message + " from gpt"