# EventHub Setup Guide

This guide provides detailed instructions for setting up the EventHub virtual event platform for development or deployment.

## Required Packages

EventHub requires the following Python packages:

```
django>=5.2.0
email-validator>=2.0.0
flask-login>=0.6.2
flask-sqlalchemy>=3.0.5
flask-wtf>=1.1.1
gunicorn>=23.0.0
pillow>=10.0.0
psycopg2-binary>=2.9.6
sqlalchemy>=2.0.19
werkzeug>=2.3.6
wtforms>=3.0.1
```

## Setup Steps

### 1. Environment Setup

#### Option A: Using Replit
If you're using Replit, the environment is already configured for you.

#### Option B: Local Setup
For local setup:

1. Create a virtual environment:
   ```
   python -m venv venv
   ```

2. Activate the virtual environment:
   - **Windows**: `venv\Scripts\activate`
   - **macOS/Linux**: `source venv/bin/activate`

3. Install required packages:
   ```
   pip install django email-validator flask-login flask-sqlalchemy flask-wtf gunicorn pillow psycopg2-binary sqlalchemy werkzeug wtforms
   ```

### 2. Database Setup

1. Apply database migrations:
   ```
   python manage.py makemigrations
   python manage.py migrate
   ```

2. Create an admin user (optional):
   ```
   python manage.py createsuperuser
   ```

### 3. Running the Application

#### Using Django's Development Server
```
python manage.py runserver 0.0.0.0:5000
```

#### Using Gunicorn (Production)
```
gunicorn --bind 0.0.0.0:5000 --reuse-port --reload main:app
```

## Folder Structure

```
eventhub/
├── accounts/           # User account management app
│   ├── migrations/     # Database migrations
│   ├── templatetags/   # Custom template tags
│   ├── admin.py        # Admin configuration
│   ├── forms.py        # Form definitions
│   ├── models.py       # Data models
│   ├── urls.py         # URL routing
│   └── views.py        # View controllers
│
├── events/             # Event management app
│   ├── migrations/     # Database migrations
│   ├── templatetags/   # Custom template tags
│   ├── admin.py        # Admin configuration
│   ├── forms.py        # Form definitions
│   ├── models.py       # Data models
│   ├── urls.py         # URL routing
│   └── views.py        # View controllers
│
├── eventhub/           # Project settings
│   ├── settings.py     # Application settings
│   ├── urls.py         # Main URL routing
│   └── wsgi.py         # WSGI configuration
│
├── static/             # Static files
│   ├── css/            # Stylesheets
│   └── js/             # JavaScript files
│
├── templates/          # HTML templates
│   ├── auth/           # Authentication templates
│   ├── events/         # Event templates
│   └── profile/        # Profile templates
│
├── main.py             # Entry point for Gunicorn
└── manage.py           # Django management script
```

## Configuration

### Static Files

Static files are configured in `eventhub/settings.py`:

```python
STATIC_URL = 'static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

### Database

The default configuration uses SQLite:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

## Troubleshooting

### Common Issues

1. **Static files not loading**: Check the static file configuration in `settings.py` and `urls.py`.

2. **Database migration errors**: Try removing the database file and running migrations again.

3. **Template errors**: Check for syntax errors in template files, particularly in template tags and filters.

### Debug Information

When troubleshooting, enable DEBUG mode in `settings.py`:

```python
DEBUG = True
```

This will provide detailed error pages with traceback information.