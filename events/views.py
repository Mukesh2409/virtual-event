from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseForbidden
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q

from .models import Event, Registration, Session, ChatMessage
from .forms import EventForm, SessionForm, ChatMessageForm
import json

def event_list(request):
    """
    Display a list of all events, with filtering
    """
    # Get search query
    search_query = request.GET.get('q', '')
    
    # Get filter parameters
    event_type = request.GET.get('type', 'all')  # all, virtual, in-person
    time_filter = request.GET.get('time', 'upcoming')  # upcoming, past, all
    
    # Base queryset
    events = Event.objects.all().order_by('start_time')
    
    # Apply search if provided
    if search_query:
        events = events.filter(
            Q(title__icontains=search_query) | 
            Q(description__icontains=search_query) |
            Q(location__icontains=search_query)
        )
    
    # Apply event type filter
    if event_type == 'virtual':
        events = events.filter(is_virtual=True)
    elif event_type == 'in-person':
        events = events.filter(is_virtual=False)
    
    # Apply time filter
    now = timezone.now()
    if time_filter == 'upcoming':
        events = events.filter(start_time__gte=now)
    elif time_filter == 'past':
        events = events.filter(end_time__lt=now)
    
    # Get featured events for the sidebar
    featured_events = Event.objects.filter(is_featured=True, start_time__gte=now)[:5]
    
    context = {
        'events': events,
        'featured_events': featured_events,
        'search_query': search_query,
        'event_type': event_type,
        'time_filter': time_filter,
    }
    return render(request, 'events/list.html', context)

def event_detail(request, event_id):
    """
    Display details for a specific event
    """
    event = get_object_or_404(Event, id=event_id)
    sessions = event.sessions.all().order_by('start_time')
    
    # Check if the user is registered
    is_registered = False
    if request.user.is_authenticated:
        is_registered = Registration.objects.filter(user=request.user, event=event).exists()
    
    # Get registration count
    registration_count = event.registrations.count()
    
    # Calculate if the event is full
    is_full = False
    if event.max_attendees and registration_count >= event.max_attendees:
        is_full = True
    
    context = {
        'event': event,
        'sessions': sessions,
        'is_registered': is_registered,
        'registration_count': registration_count,
        'is_full': is_full,
        'is_creator': request.user == event.creator,
    }
    return render(request, 'events/details.html', context)

@login_required
def event_create(request):
    """
    Create a new event
    """
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.creator = request.user
            event.save()
            messages.success(request, 'Event created successfully!')
            return redirect('events:event_detail', event_id=event.id)
    else:
        form = EventForm()
    
    context = {
        'form': form,
        'is_creating': True,
    }
    return render(request, 'events/create.html', context)

@login_required
def event_edit(request, event_id):
    """
    Edit an existing event
    """
    event = get_object_or_404(Event, id=event_id)
    
    # Check if the user is the creator
    if request.user != event.creator:
        messages.error(request, 'You do not have permission to edit this event.')
        return redirect('events:event_detail', event_id=event.id)
    
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, 'Event updated successfully!')
            return redirect('events:event_detail', event_id=event.id)
    else:
        form = EventForm(instance=event)
    
    context = {
        'form': form,
        'event': event,
        'is_creating': False,
    }
    return render(request, 'events/create.html', context)

@login_required
def event_delete(request, event_id):
    """
    Delete an event
    """
    event = get_object_or_404(Event, id=event_id)
    
    # Check if the user is the creator
    if request.user != event.creator:
        messages.error(request, 'You do not have permission to delete this event.')
        return redirect('events:event_detail', event_id=event.id)
    
    if request.method == 'POST':
        event.delete()
        messages.success(request, 'Event deleted successfully!')
        return redirect('events:my_events')
    
    context = {
        'event': event,
    }
    return render(request, 'events/delete.html', context)

@login_required
def event_register(request, event_id):
    """
    Register for an event
    """
    event = get_object_or_404(Event, id=event_id)
    
    # Check if the user is already registered
    if Registration.objects.filter(user=request.user, event=event).exists():
        messages.info(request, 'You are already registered for this event.')
        return redirect('events:event_detail', event_id=event.id)
    
    # Check if the event is full
    if event.max_attendees and event.registrations.count() >= event.max_attendees:
        messages.error(request, 'This event is full.')
        return redirect('events:event_detail', event_id=event.id)
    
    # Create the registration
    Registration.objects.create(user=request.user, event=event)
    messages.success(request, f'You have successfully registered for {event.title}!')
    
    return redirect('events:event_detail', event_id=event.id)

@login_required
def event_unregister(request, event_id):
    """
    Unregister from an event
    """
    event = get_object_or_404(Event, id=event_id)
    
    # Check if the user is registered
    registration = Registration.objects.filter(user=request.user, event=event).first()
    if not registration:
        messages.info(request, 'You are not registered for this event.')
        return redirect('events:event_detail', event_id=event.id)
    
    # Delete the registration
    registration.delete()
    messages.success(request, f'You have unregistered from {event.title}.')
    
    return redirect('events:event_detail', event_id=event.id)

@login_required
def my_events(request):
    """
    View events created by the current user and events they're registered for
    """
    # Get events created by the user
    created_events = Event.objects.filter(creator=request.user).order_by('start_time')
    
    # Get events the user is registered for
    registrations = Registration.objects.filter(user=request.user).select_related('event')
    registered_events = [reg.event for reg in registrations]
    
    context = {
        'created_events': created_events,
        'registered_events': registered_events,
    }
    return render(request, 'events/my_events.html', context)

@login_required
def event_manage(request, event_id):
    """
    Manage an event (sessions, attendees, etc.)
    """
    event = get_object_or_404(Event, id=event_id)
    
    # Check if the user is the creator
    if request.user != event.creator:
        messages.error(request, 'You do not have permission to manage this event.')
        return redirect('events:event_detail', event_id=event.id)
    
    # Get sessions and registrations
    sessions = event.sessions.all().order_by('start_time')
    registrations = event.registrations.all().select_related('user').order_by('registration_date')
    
    context = {
        'event': event,
        'sessions': sessions,
        'registrations': registrations,
    }
    return render(request, 'events/manage.html', context)

@login_required
def add_session(request, event_id):
    """
    Add a session to an event
    """
    event = get_object_or_404(Event, id=event_id)
    
    # Check if the user is the creator
    if request.user != event.creator:
        messages.error(request, 'You do not have permission to add sessions to this event.')
        return redirect('events:event_detail', event_id=event.id)
    
    if request.method == 'POST':
        form = SessionForm(request.POST, event=event)
        if form.is_valid():
            session = form.save(commit=False)
            session.event = event
            session.save()
            messages.success(request, 'Session added successfully!')
            return redirect('events:event_manage', event_id=event.id)
    else:
        form = SessionForm(event=event)
    
    context = {
        'form': form,
        'event': event,
    }
    return render(request, 'events/session_add.html', context)

@login_required
def delete_session(request, event_id, session_id):
    """
    Delete a session from an event
    """
    event = get_object_or_404(Event, id=event_id)
    session = get_object_or_404(Session, id=session_id, event=event)
    
    # Check if the user is the creator
    if request.user != event.creator:
        messages.error(request, 'You do not have permission to delete sessions from this event.')
        return redirect('events:event_detail', event_id=event.id)
    
    if request.method == 'POST':
        session.delete()
        messages.success(request, 'Session deleted successfully!')
        return redirect('events:event_manage', event_id=event.id)
    
    context = {
        'session': session,
        'event': event,
    }
    return render(request, 'events/session_delete.html', context)

@login_required
def livestream(request, event_id):
    """
    View an event's livestream
    """
    event = get_object_or_404(Event, id=event_id)
    
    # Check if the user is registered
    if not Registration.objects.filter(user=request.user, event=event).exists():
        messages.error(request, 'You must be registered for this event to access the livestream.')
        return redirect('events:event_detail', event_id=event.id)
    
    # Check if the event is virtual
    if not event.is_virtual:
        messages.error(request, 'This event does not have a livestream.')
        return redirect('events:event_detail', event_id=event.id)
    
    chat_form = ChatMessageForm()
    
    context = {
        'event': event,
        'chat_form': chat_form,
    }
    return render(request, 'events/livestream.html', context)

@login_required
def send_chat(request, event_id):
    """
    Send a chat message for an event livestream
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST method allowed'}, status=405)
    
    event = get_object_or_404(Event, id=event_id)
    
    # Check if the user is registered
    if not Registration.objects.filter(user=request.user, event=event).exists():
        return JsonResponse({'error': 'You must be registered for this event to send messages'}, status=403)
    
    try:
        data = json.loads(request.body)
        message_text = data.get('message', '').strip()
        
        if not message_text:
            return JsonResponse({'error': 'Message cannot be empty'}, status=400)
        
        # Create the message
        message = ChatMessage.objects.create(
            event=event,
            user=request.user,
            message=message_text
        )
        
        # Return the message data
        return JsonResponse({
            'id': message.id,
            'username': request.user.username,
            'message': message.message,
            'timestamp': message.timestamp.strftime('%H:%M')
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@login_required
def get_chat_messages(request, event_id):
    """
    Get chat messages for an event livestream
    """
    event = get_object_or_404(Event, id=event_id)
    
    # Check if the user is registered
    if not Registration.objects.filter(user=request.user, event=event).exists():
        return JsonResponse({'error': 'You must be registered for this event to view messages'}, status=403)
    
    # Get the last message ID the client has
    last_id = request.GET.get('last_id', 0)
    try:
        last_id = int(last_id)
    except:
        last_id = 0
    
    # Get new messages
    messages = ChatMessage.objects.filter(event=event, id__gt=last_id).select_related('user')[:50]
    
    # Format the messages
    message_list = [{
        'id': msg.id,
        'username': msg.user.username,
        'message': msg.message,
        'timestamp': msg.timestamp.strftime('%H:%M')
    } for msg in messages]
    
    return JsonResponse(message_list, safe=False)
