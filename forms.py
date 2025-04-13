from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, BooleanField, DateTimeField, IntegerField, SelectField, URLField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, URL, Optional, ValidationError
from datetime import datetime
from models import User

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=64)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    first_name = StringField('First Name', validators=[Optional(), Length(max=64)])
    last_name = StringField('Last Name', validators=[Optional(), Length(max=64)])
    submit = SubmitField('Register')
    
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is already taken. Please choose a different one.')
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is already registered. Please use a different one.')


class ProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=64)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    first_name = StringField('First Name', validators=[Optional(), Length(max=64)])
    last_name = StringField('Last Name', validators=[Optional(), Length(max=64)])
    bio = TextAreaField('Bio', validators=[Optional()])
    submit = SubmitField('Update Profile')
    
    def __init__(self, original_username, original_email, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username
        self.original_email = original_email
    
    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is already taken. Please choose a different one.')
    
    def validate_email(self, email):
        if email.data != self.original_email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is already registered. Please use a different one.')


class EventForm(FlaskForm):
    title = StringField('Event Title', validators=[DataRequired(), Length(max=128)])
    description = TextAreaField('Description', validators=[DataRequired()])
    start_time = DateTimeField('Start Time', validators=[DataRequired()], format='%Y-%m-%dT%H:%M')
    end_time = DateTimeField('End Time', validators=[DataRequired()], format='%Y-%m-%dT%H:%M')
    location = StringField('Location', validators=[Optional(), Length(max=128)])
    is_virtual = BooleanField('Virtual Event')
    stream_url = URLField('Stream URL', validators=[Optional(), URL()])
    max_attendees = IntegerField('Maximum Attendees', validators=[Optional()])
    is_featured = BooleanField('Feature this Event')
    image_url = URLField('Event Image URL', validators=[Optional(), URL()])
    submit = SubmitField('Create Event')
    
    def validate_end_time(self, end_time):
        if end_time.data < self.start_time.data:
            raise ValidationError('End time must be after start time.')


class SessionForm(FlaskForm):
    title = StringField('Session Title', validators=[DataRequired(), Length(max=128)])
    description = TextAreaField('Description', validators=[Optional()])
    start_time = DateTimeField('Start Time', validators=[DataRequired()], format='%Y-%m-%dT%H:%M')
    end_time = DateTimeField('End Time', validators=[DataRequired()], format='%Y-%m-%dT%H:%M')
    speaker = StringField('Speaker', validators=[Optional(), Length(max=128)])
    submit = SubmitField('Add Session')
    
    def validate_end_time(self, end_time):
        if end_time.data < self.start_time.data:
            raise ValidationError('End time must be after start time.')


class ChatMessageForm(FlaskForm):
    message = TextAreaField('Message', validators=[DataRequired()])
    submit = SubmitField('Send')
