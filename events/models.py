from django.db import models
from django.conf import settings
from django.utils import timezone

class Event(models.Model):
    """
    Model representing an event
    """
    title = models.CharField(max_length=128)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        related_name='events_created'
    )
    location = models.CharField(max_length=128, blank=True, null=True)
    is_virtual = models.BooleanField(default=True)
    stream_url = models.URLField(max_length=256, blank=True, null=True)
    max_attendees = models.PositiveIntegerField(blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    image_url = models.URLField(max_length=256, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title

class Registration(models.Model):
    """
    Model representing a user's registration for an event
    """
    STATUS_CHOICES = (
        ('registered', 'Registered'),
        ('attended', 'Attended'),
        ('canceled', 'Canceled'),
    )
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        related_name='registrations'
    )
    event = models.ForeignKey(
        Event, 
        on_delete=models.CASCADE,
        related_name='registrations'
    )
    registration_date = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='registered')
    
    def __str__(self):
        return f'{self.user.username} - {self.event.title}'
    
    class Meta:
        unique_together = ('user', 'event')

class Session(models.Model):
    """
    Model representing a session within an event
    """
    event = models.ForeignKey(
        Event, 
        on_delete=models.CASCADE,
        related_name='sessions'
    )
    title = models.CharField(max_length=128)
    description = models.TextField(blank=True, null=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    speaker = models.CharField(max_length=128, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title

class ChatMessage(models.Model):
    """
    Model representing a chat message in an event
    """
    event = models.ForeignKey(
        Event, 
        on_delete=models.CASCADE,
        related_name='chat_messages'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        related_name='chat_messages'
    )
    message = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f'{self.user.username}: {self.message[:20]}...'
        
    class Meta:
        ordering = ['timestamp']
