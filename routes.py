from flask import render_template, redirect, url_for, flash, request, jsonify, abort
from flask_login import login_user, current_user, logout_user, login_required
from app import app, db
from models import User, Event, Registration, Session, ChatMessage
from forms import LoginForm, RegistrationForm, ProfileForm, EventForm, SessionForm, ChatMessageForm
from datetime import datetime
from utils import save_picture
import logging

# Home/landing page route
@app.route('/')
def index():
    featured_events = Event.query.filter_by(is_featured=True).order_by(Event.start_time).limit(6).all()
    upcoming_events = Event.query.filter(Event.start_time > datetime.utcnow()).order_by(Event.start_time).limit(10).all()
    return render_template('index.html', featured_events=featured_events, upcoming_events=upcoming_events)


# Authentication routes
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page if next_page else url_for('index'))
        else:
            flash('Login unsuccessful. Please check email and password.', 'danger')
    
    return render_template('auth/login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data
        )
        user.set_password(form.password.data)
        
        db.session.add(user)
        db.session.commit()
        
        flash('Your account has been created! You can now log in.', 'success')
        return redirect(url_for('login'))
    
    return render_template('auth/register.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


# Profile routes
@app.route('/profile')
@login_required
def profile():
    return render_template('profile/view.html', user=current_user)


@app.route('/profile/edit', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = ProfileForm(current_user.username, current_user.email)
    
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        current_user.bio = form.bio.data
        
        db.session.commit()
        flash('Your profile has been updated!', 'success')
        return redirect(url_for('profile'))
    
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
        form.bio.data = current_user.bio
    
    return render_template('profile/edit.html', form=form)


# Event routes
@app.route('/events')
def events():
    page = request.args.get('page', 1, type=int)
    events = Event.query.filter(Event.start_time > datetime.utcnow()).order_by(Event.start_time).paginate(page=page, per_page=12)
    return render_template('events/list.html', events=events)


@app.route('/events/create', methods=['GET', 'POST'])
@login_required
def create_event():
    form = EventForm()
    
    if form.validate_on_submit():
        event = Event(
            title=form.title.data,
            description=form.description.data,
            start_time=form.start_time.data,
            end_time=form.end_time.data,
            location=form.location.data,
            is_virtual=form.is_virtual.data,
            stream_url=form.stream_url.data,
            max_attendees=form.max_attendees.data,
            is_featured=form.is_featured.data,
            image_url=form.image_url.data,
            creator=current_user
        )
        
        db.session.add(event)
        db.session.commit()
        
        flash('Your event has been created!', 'success')
        return redirect(url_for('event_details', event_id=event.id))
    
    return render_template('events/create.html', form=form)


@app.route('/events/<int:event_id>')
def event_details(event_id):
    event = Event.query.get_or_404(event_id)
    sessions = Session.query.filter_by(event_id=event_id).order_by(Session.start_time).all()
    
    is_registered = False
    if current_user.is_authenticated:
        registration = Registration.query.filter_by(user_id=current_user.id, event_id=event_id).first()
        is_registered = registration is not None
    
    return render_template('events/details.html', event=event, sessions=sessions, is_registered=is_registered)


@app.route('/events/<int:event_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_event(event_id):
    event = Event.query.get_or_404(event_id)
    
    # Check if current user is the creator of the event
    if event.creator_id != current_user.id:
        abort(403)
    
    form = EventForm()
    
    if form.validate_on_submit():
        event.title = form.title.data
        event.description = form.description.data
        event.start_time = form.start_time.data
        event.end_time = form.end_time.data
        event.location = form.location.data
        event.is_virtual = form.is_virtual.data
        event.stream_url = form.stream_url.data
        event.max_attendees = form.max_attendees.data
        event.is_featured = form.is_featured.data
        event.image_url = form.image_url.data
        
        db.session.commit()
        
        flash('Your event has been updated!', 'success')
        return redirect(url_for('event_details', event_id=event.id))
    
    elif request.method == 'GET':
        form.title.data = event.title
        form.description.data = event.description
        form.start_time.data = event.start_time
        form.end_time.data = event.end_time
        form.location.data = event.location
        form.is_virtual.data = event.is_virtual
        form.stream_url.data = event.stream_url
        form.max_attendees.data = event.max_attendees
        form.is_featured.data = event.is_featured
        form.image_url.data = event.image_url
    
    return render_template('events/create.html', form=form, edit_mode=True)


@app.route('/events/<int:event_id>/delete', methods=['POST'])
@login_required
def delete_event(event_id):
    event = Event.query.get_or_404(event_id)
    
    # Check if current user is the creator of the event
    if event.creator_id != current_user.id:
        abort(403)
    
    db.session.delete(event)
    db.session.commit()
    
    flash('Your event has been deleted!', 'success')
    return redirect(url_for('events'))


@app.route('/events/<int:event_id>/register', methods=['POST'])
@login_required
def register_event(event_id):
    event = Event.query.get_or_404(event_id)
    
    # Check if user is already registered
    existing_registration = Registration.query.filter_by(user_id=current_user.id, event_id=event_id).first()
    if existing_registration:
        flash('You are already registered for this event!', 'info')
        return redirect(url_for('event_details', event_id=event_id))
    
    # Check if event has reached max capacity
    if event.max_attendees and event.registrations.count() >= event.max_attendees:
        flash('This event has reached maximum capacity!', 'danger')
        return redirect(url_for('event_details', event_id=event_id))
    
    registration = Registration(user_id=current_user.id, event_id=event_id)
    db.session.add(registration)
    db.session.commit()
    
    flash('You have successfully registered for this event!', 'success')
    return redirect(url_for('event_details', event_id=event_id))


@app.route('/events/<int:event_id>/unregister', methods=['POST'])
@login_required
def unregister_event(event_id):
    registration = Registration.query.filter_by(user_id=current_user.id, event_id=event_id).first_or_404()
    
    db.session.delete(registration)
    db.session.commit()
    
    flash('You have successfully unregistered from this event!', 'success')
    return redirect(url_for('event_details', event_id=event_id))


@app.route('/events/<int:event_id>/manage')
@login_required
def manage_event(event_id):
    event = Event.query.get_or_404(event_id)
    
    # Check if current user is the creator of the event
    if event.creator_id != current_user.id:
        abort(403)
    
    registrations = Registration.query.filter_by(event_id=event_id).all()
    sessions = Session.query.filter_by(event_id=event_id).order_by(Session.start_time).all()
    session_form = SessionForm()
    
    return render_template('events/manage.html', event=event, registrations=registrations, sessions=sessions, session_form=session_form)


@app.route('/events/<int:event_id>/sessions/add', methods=['POST'])
@login_required
def add_session(event_id):
    event = Event.query.get_or_404(event_id)
    
    # Check if current user is the creator of the event
    if event.creator_id != current_user.id:
        abort(403)
    
    form = SessionForm()
    
    if form.validate_on_submit():
        session = Session(
            event_id=event_id,
            title=form.title.data,
            description=form.description.data,
            start_time=form.start_time.data,
            end_time=form.end_time.data,
            speaker=form.speaker.data
        )
        
        db.session.add(session)
        db.session.commit()
        
        flash('Session has been added!', 'success')
    
    return redirect(url_for('manage_event', event_id=event_id))


@app.route('/events/<int:event_id>/sessions/<int:session_id>/delete', methods=['POST'])
@login_required
def delete_session(event_id, session_id):
    event = Event.query.get_or_404(event_id)
    session = Session.query.get_or_404(session_id)
    
    # Check if current user is the creator of the event
    if event.creator_id != current_user.id:
        abort(403)
    
    db.session.delete(session)
    db.session.commit()
    
    flash('Session has been deleted!', 'success')
    return redirect(url_for('manage_event', event_id=event_id))


# Livestream and chat routes
@app.route('/events/<int:event_id>/livestream')
@login_required
def livestream(event_id):
    event = Event.query.get_or_404(event_id)
    
    # Check if user is registered for the event
    registration = Registration.query.filter_by(user_id=current_user.id, event_id=event_id).first()
    if not registration and event.creator_id != current_user.id:
        flash('You must be registered for this event to access the livestream!', 'danger')
        return redirect(url_for('event_details', event_id=event_id))
    
    chat_form = ChatMessageForm()
    return render_template('events/livestream.html', event=event, chat_form=chat_form)


@app.route('/events/<int:event_id>/chat/send', methods=['POST'])
@login_required
def send_chat(event_id):
    event = Event.query.get_or_404(event_id)
    
    # Check if user is registered for the event
    registration = Registration.query.filter_by(user_id=current_user.id, event_id=event_id).first()
    if not registration and event.creator_id != current_user.id:
        return jsonify({'error': 'You must be registered for this event to participate in chat'}), 403
    
    form = ChatMessageForm()
    
    if form.validate_on_submit():
        message = ChatMessage(
            event_id=event_id,
            user_id=current_user.id,
            message=form.message.data
        )
        
        db.session.add(message)
        db.session.commit()
        
        return jsonify({
            'id': message.id,
            'username': current_user.username,
            'message': message.message,
            'timestamp': message.timestamp.strftime('%H:%M')
        })
    
    return jsonify({'error': 'Invalid message'}), 400


@app.route('/events/<int:event_id>/chat/messages')
@login_required
def get_chat_messages(event_id):
    event = Event.query.get_or_404(event_id)
    
    # Check if user is registered for the event
    registration = Registration.query.filter_by(user_id=current_user.id, event_id=event_id).first()
    if not registration and event.creator_id != current_user.id:
        return jsonify({'error': 'You must be registered for this event to view chat'}), 403
    
    last_id = request.args.get('last_id', 0, type=int)
    messages = ChatMessage.query.filter(ChatMessage.event_id == event_id, ChatMessage.id > last_id).order_by(ChatMessage.timestamp).all()
    
    return jsonify([{
        'id': msg.id,
        'username': msg.user.username,
        'message': msg.message,
        'timestamp': msg.timestamp.strftime('%H:%M')
    } for msg in messages])


# My Events Route
@app.route('/my-events')
@login_required
def my_events():
    created_events = Event.query.filter_by(creator_id=current_user.id).order_by(Event.start_time).all()
    registered_events = Event.query.join(Registration).filter(Registration.user_id == current_user.id).order_by(Event.start_time).all()
    
    return render_template('events/my_events.html', created_events=created_events, registered_events=registered_events)


# Error handlers
@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


@app.errorhandler(403)
def forbidden_error(error):
    return render_template('errors/403.html'), 403


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('errors/500.html'), 500
