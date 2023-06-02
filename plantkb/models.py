from django.db import models

# Create your models here.

# plant knowledge base model
class Plant(models.Model):
    plant_name = models.CharField(max_length=30)
    plant_healthy_top_leaf_image = models.ImageField(upload_to='plants')
    plant_healthy_bottom_leaf_image = models.ImageField(upload_to='plants')
    date_created = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.plant_name

    class Meta:
        ordering = ['-date_created']

class Disease(models.Model):
    disease_name = models.CharField(max_length=30)
    disease_plant = models.ForeignKey(Plant, on_delete=models.CASCADE)
    # disease_diseased_top_leaf_image = models.ImageField(upload_to='diseases')
    # disease_diseased_bottom_leaf_image = models.ImageField(upload_to='diseases')
    date_created = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.disease_name

    class Meta:
        ordering = ['-date_created']

class DiseaseSymptom(models.Model):
    disease_symptom_name = models.CharField(max_length=30)
    disease_name = models.ForeignKey(Disease, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.disease_symptom_name

    class Meta:
        ordering = ['-date_created']

class DiseaseCause(models.Model):
    disease_cause_name = models.CharField(max_length=30)
    disease_name = models.ForeignKey(Disease, on_delete=models.CASCADE)
    temperature = models.IntegerField()
    humidity = models.IntegerField()
    wind_speed = models.IntegerField()
    rainfall = models.IntegerField()
    date_created = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.disease_cause_name

    class Meta:
        ordering = ['-date_created']

class Treatment(models.Model):
    treatment_title = models.CharField(max_length=30)
    treatment_disease = models.ForeignKey(Disease, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.treatment_title

    class Meta:
        ordering = ['-date_created']

class TreatmentStep(models.Model):
    treatment_step_title = models.CharField(max_length=30)
    treatment_name = models.ForeignKey(Treatment, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.treatment_step_title

    class Meta:
        ordering = ['-date_created']