from django import forms
from .models import Event, Session, ChatMessage
from django.core.exceptions import ValidationError
from django.utils import timezone

class EventForm(forms.ModelForm):
    """
    Form for creating and editing events
    """
    class Meta:
        model = Event
        fields = ['title', 'description', 'start_time', 'end_time', 'location', 
                  'is_virtual', 'stream_url', 'max_attendees', 'is_featured', 'image_url']
        widgets = {
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'description': forms.Textarea(attrs={'rows': 5}),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')
        
        if start_time and end_time:
            # Check if end_time is after start_time
            if end_time <= start_time:
                raise ValidationError("End time must be after start time")
                
            # Check if start_time is in the future for new events
            if not self.instance.pk and start_time < timezone.now():
                raise ValidationError("Start time cannot be in the past for new events")
                
        return cleaned_data
        
class SessionForm(forms.ModelForm):
    """
    Form for creating and editing event sessions
    """
    class Meta:
        model = Session
        fields = ['title', 'description', 'start_time', 'end_time', 'speaker']
        widgets = {
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, event=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.event = event
        
    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')
        
        if start_time and end_time:
            # Check if end_time is after start_time
            if end_time <= start_time:
                raise ValidationError("End time must be after start time")
                
            # Check if session is within event time frame (if event is provided)
            if self.event:
                if start_time < self.event.start_time:
                    raise ValidationError("Session cannot start before the event starts")
                
                if end_time > self.event.end_time:
                    raise ValidationError("Session cannot end after the event ends")
                    
        return cleaned_data

class ChatMessageForm(forms.ModelForm):
    """
    Form for creating chat messages
    """
    class Meta:
        model = ChatMessage
        fields = ['message']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Type your message here...'}),
        }