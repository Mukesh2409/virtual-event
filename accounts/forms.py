from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()

class UserRegisterForm(UserCreationForm):
    """
    Form for registering a new user
    Extends Django's UserCreationForm to include email
    """
    email = forms.EmailField()
    first_name = forms.CharField(max_length=64, required=False)
    last_name = forms.CharField(max_length=64, required=False)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']
        
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("A user with that email already exists.")
        return email

class UserUpdateForm(forms.ModelForm):
    """
    Form for updating an existing user's profile
    """
    email = forms.EmailField()
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'bio']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initial_username = self.instance.username
        self.initial_email = self.instance.email
        
    def clean_username(self):
        username = self.cleaned_data.get('username')
        # Only validate if username has changed
        if username != self.initial_username:
            if User.objects.filter(username=username).exists():
                raise ValidationError("That username is already taken.")
        return username
        
    def clean_email(self):
        email = self.cleaned_data.get('email')
        # Only validate if email has changed
        if email != self.initial_email:
            if User.objects.filter(email=email).exists():
                raise ValidationError("A user with that email already exists.")
        return email