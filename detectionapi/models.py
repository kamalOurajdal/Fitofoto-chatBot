from django.db import models
from farmers.models import Farmer
from subscription.models import UserSubscription
# Create your models here.

# Deep learning detection model

class AIDetection(models.Model):
    detection_farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE)
    detection_subscription = models.ForeignKey(UserSubscription, on_delete=models.CASCADE)
    detection_plant_name = models.CharField(max_length=30)
    detection_disease_name = models.CharField(max_length=30)
    detection_treatments = models.CharField(max_length=30)
    detection_diseased_top_leaf_image = models.ImageField(upload_to='detections')
    detection_diseased_bottom_leaf_image = models.ImageField(upload_to='detections')
    detection_latitude = models.CharField(max_length=30)
    detection_longitude = models.CharField(max_length=30)
    detection_temperature = models.IntegerField()
    detection_humidity = models.IntegerField()
    detection_wind_speed = models.IntegerField()
    detection_rainfall = models.IntegerField()
    detection_accuracy = models.IntegerField()
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "DET-"+str(self.date_created)
    
    class Meta:
        ordering = ['-date_created']