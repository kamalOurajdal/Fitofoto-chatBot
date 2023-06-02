from django.db import models
from experts.models import Expert
from farmers.models import Farmer
from subscription.models import UserSubscription
from plantkb.models import Plant, Disease, Treatment
# Create your models here.

class ExpertDetection(models.Model):
    detection_expert = models.ForeignKey(Expert, on_delete=models.CASCADE)
    detection_farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE)
    detection_subscription = models.ForeignKey(UserSubscription, on_delete=models.CASCADE)
    detection_plant_name = models.ForeignKey(Plant, on_delete=models.CASCADE)
    detection_disease_name = models.ForeignKey(Disease, on_delete=models.CASCADE)
    detection_treatments = models.ManyToManyField(Treatment)
    # detection_diseased_top_leaf_image = models.ImageField(upload_to='detections')
    # detection_diseased_bottom_leaf_image = models.ImageField(upload_to='detections')
    detection_latitude = models.CharField(max_length=30)
    detection_longitude = models.CharField(max_length=30)
    detection_temperature = models.IntegerField()
    detection_humidity = models.IntegerField()
    detection_wind_speed = models.IntegerField()
    detection_rainfall = models.IntegerField()
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "DET-"+str(self.date_created)
    
    class Meta:
        ordering = ['-date_created']

# store when the detections reach 100,000 records in one plant to trigger the training of the model new version
class AIModel(models.Model):
    detection_plant_name = models.ForeignKey(Plant, on_delete=models.CASCADE)
    detection_count = models.IntegerField(default=100000)
    ai_model_version = models.FloatField()
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "DET-"+str(self.date_created)
    
    class Meta:
        ordering = ['-date_created']