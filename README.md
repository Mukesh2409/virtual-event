# EventHub - Virtual Event Hosting Platform

EventHub is a comprehensive virtual event hosting platform built with Django and SQLite, featuring live streaming, attendee registration, chat functionality, and event scheduling capabilities.

## Features

- **User Management**: Create an account, manage your profile, and login/logout
- **Event Creation**: Create, edit, and delete events with detailed information
- **Event Registration**: Register for events and manage your registrations
- **Live Streaming**: Virtual events with live streaming capabilities
- **Chat System**: Real-time chat functionality during events
- **Session Management**: Create and manage multiple sessions within an event

## Prerequisites

- Python 3.8 or higher
- Django 5.2 or higher
- SQLite (included with Django)

## Setup & Installation

1. **Clone the repository**:
   ```
   git clone <repository-url>
   cd eventhub
   ```

2. **Install dependencies**:
   ```
   pip install -r requirements.txt
   ```

3. **Apply database migrations**:
   ```
   python manage.py makemigrations
   python manage.py migrate
   ```

4. **Run the application**:
   ```
   python manage.py runserver 0.0.0.0:5000
   ```
   or
   ```
   gunicorn --bind 0.0.0.0:5000 --reuse-port --reload main:app
   ```

5. **Access the application** in your browser at:
   ```
   http://localhost:5000
   ```

## Using the Application

### User Management

1. **Register**: Create a new account by providing username, email, and password
2. **Login**: Sign in with your credentials
3. **Profile**: View and edit your profile information

### Event Management

1. **View Events**: Browse all available events on the platform
2. **Create Event**: Create a new event with details like title, description, time, location, etc.
3. **My Events**: View events you've created or registered for
4. **Manage Event**: Add sessions, view attendees, and manage event details

### Attending Events

1. **Register for Event**: Sign up to attend an event
2. **Join Livestream**: Access the virtual event through the livestream page
3. **Chat**: Participate in the event chat during livestreams

## Project Structure

```
eventhub/
├── accounts/           # User account management app
├── events/             # Event management app
├── eventhub/           # Main project settings
├── static/             # Static files (CSS, JS)
├── templates/          # HTML templates
├── manage.py           # Django management script
└── main.py             # Entry point for Gunicorn
```

## Development

### Setting up a development environment

1. Clone the repository
2. Create a virtual environment: `python -m venv venv`
3. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - macOS/Linux: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Apply migrations: `python manage.py migrate`
6. Run the development server: `python manage.py runserver`

### Creating a superuser (admin)

To access the admin interface:

```
python manage.py createsuperuser
```

Follow the prompts to create an admin user, then access the admin panel at `/admin`.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Built with Django and Tailwind CSS
- Icons from Font Awesome