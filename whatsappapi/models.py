from django.db import models

# Create your models here.

# store conversations as instance
class Conversation(models.Model):
    phone_number = models.CharField(max_length=20)
    # conversation type can be expert or farmer
    conversation_type = models.CharField(choices=(('expert', 'expert'), ('farmer', 'farmer')), max_length=10)
    date_created = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.phone_number
    
    class Meta:
        ordering = ['-date_created']

# store text messages
class TextMessage(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)
    message = models.CharField(max_length=1000)
    date_created = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.message
    
    class Meta:
        ordering = ['-date_created']

# store image messages
class ImageMessage(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)
    media_message = models.ImageField(upload_to='media_messages')
    date_created = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.media_message
    
    class Meta:
        ordering = ['-date_created']

# store audio messages
class AudioMessage(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)
    audio_message = models.FileField(upload_to='audio_messages')
    date_created = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.audio_message
    
    class Meta:
        ordering = ['-date_created']

# store video messages
class VideoMessage(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)
    video_message = models.FileField(upload_to='video_messages')
    date_created = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.video_message
    
    class Meta:
        ordering = ['-date_created']

# store document messages
class DocumentMessage(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)
    document_message = models.FileField(upload_to='document_messages')
    date_created = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.document_message
    
    class Meta:
        ordering = ['-date_created']

# store location messages
class LocationMessage(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)
    latitude = models.CharField(max_length=30)
    longitude = models.CharField(max_length=30)
    date_created = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.latitude
    
    class Meta:
        ordering = ['-date_created']

# store contact messages
class ContactMessage(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)
    contact_name = models.CharField(max_length=30)
    contact_number = models.CharField(max_length=20)
    date_created = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.contact_name
    
    class Meta:
        ordering = ['-date_created']
