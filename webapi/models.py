from django.db import models
from django.forms import forms


# Create your models here.
class ImageUploadForm(models.Model):
    image = models.ImageField(upload_to='images')