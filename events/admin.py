from django.contrib import admin
from .models import Event, Registration, Session, ChatMessage

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_time', 'end_time', 'creator', 'is_virtual', 'is_featured')
    list_filter = ('is_virtual', 'is_featured', 'start_time')
    search_fields = ('title', 'description', 'location')
    date_hierarchy = 'start_time'

@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = ('user', 'event', 'registration_date', 'status')
    list_filter = ('status', 'registration_date')
    search_fields = ('user__username', 'event__title')

@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ('title', 'event', 'start_time', 'end_time', 'speaker')
    list_filter = ('start_time', 'event')
    search_fields = ('title', 'description', 'speaker')

@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('user', 'event', 'timestamp', 'message_preview')
    list_filter = ('timestamp', 'event')
    search_fields = ('message', 'user__username')
    
    def message_preview(self, obj):
        return obj.message[:50] + '...' if len(obj.message) > 50 else obj.message
    
    message_preview.short_description = 'Message'
