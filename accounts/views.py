from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm
from events.models import Event, Registration

def register(request):
    """
    Register a new user
    """
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Your account has been created! You are now logged in.')
            return redirect('events:event_list')
    else:
        form = UserRegisterForm()
    
    return render(request, 'auth/register.html', {'form': form})

@login_required
def profile_view(request):
    """
    View the current user's profile
    """
    # Get user's registered events
    registrations = Registration.objects.filter(user=request.user).select_related('event')
    
    context = {
        'user': request.user,
        'registrations': registrations
    }
    return render(request, 'profile/view.html', context)

@login_required
def profile_edit(request):
    """
    Edit the current user's profile
    """
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('accounts:profile')
    else:
        form = UserUpdateForm(instance=request.user)
    
    context = {
        'form': form
    }
    return render(request, 'profile/edit.html', context)
