from django.db import models
from farmers.models import Farmer

# Create your models here.
# Subscription model
class Subscription(models.Model):
    plan_name = models.CharField(max_length=30)
    hourly_price = models.IntegerField()
    daily_limit = models.IntegerField()
    detections_balance = models.IntegerField()
    date_created = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.plan_name

class UserSubscription(models.Model):
    farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE)
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.farmer.phone_number

class SubscriptionPayment(models.Model):
    user_subscription = models.ForeignKey(UserSubscription, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    amount = models.IntegerField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.user_subscription.farmer.phone_number

# Pay as you go model
class PayAsYouGoPlan(models.Model):
    plan_name = models.CharField(max_length=30)
    detection_price = models.IntegerField()
    daily_limit = models.IntegerField()
    date_created = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.plan_name
    
class UserPayAsYouGoPlan(models.Model):
    farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE)
    pay_as_you_go_plan = models.ForeignKey(PayAsYouGoPlan, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.farmer.phone_number
    
class PayAsYouGoPayment(models.Model):
    user_pay_as_you_go_plan = models.ForeignKey(UserPayAsYouGoPlan, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    amount = models.IntegerField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.user_pay_as_you_go_plan.farmer.phone_number
