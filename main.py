import os
import sys
import logging
from eventhub.wsgi import application as django_application

# Set up logging for debugging
logging.basicConfig(level=logging.DEBUG)

# Export the app for Gunicorn
app = django_application

# Run Django development server
if __name__ == "__main__":
    from django.core.management import execute_from_command_line
    execute_from_command_line(["manage.py", "runserver", "0.0.0.0:5000"])
