# Running EventHub on Replit

This guide provides specific instructions for running the EventHub virtual event platform on the Replit environment.

## Replit Setup

1. **Fork the Repl**: If you're viewing this project on Replit, click the "Fork" button to create your own copy.

2. **Update Dependencies**: Make sure all required packages are installed by running:
   ```
   pip install -r requirements.txt
   ```
   
   Or you can install them individually:
   ```
   pip install django flask-login flask-sqlalchemy flask-wtf gunicorn pillow psycopg2-binary sqlalchemy werkzeug wtforms email-validator
   ```

3. **Database Setup**: Run database migrations to set up the SQLite database:
   ```
   python manage.py makemigrations
   python manage.py migrate
   ```

4. **Create an Admin User** (optional):
   ```
   python manage.py createsuperuser
   ```

## Running the Application

EventHub on Replit can be run using either of the following methods:

### Method 1: Using the Workflow (Recommended)

1. Go to the "Workflows" tab in Replit
2. Click the "Start application" workflow 
3. This will start the Gunicorn server with the proper settings

### Method 2: Run Command

1. Click the "Run" button in Replit
2. This will execute the command defined in the `.replit` file:
   ```
   gunicorn --bind 0.0.0.0:5000 --reuse-port --reload main:app
   ```

## Accessing the Application

Once the application is running:

1. Click on the "Webview" tab to view the application in the embedded browser
2. Alternatively, click the URL shown in the console output to open the app in a new browser tab

## Troubleshooting

### Static Files Not Loading

If you experience issues with static files (CSS/JS) not loading:

1. Check that `eventhub/settings.py` has the proper static file configuration:
   ```python
   STATIC_URL = 'static/'
   STATICFILES_DIRS = [
       BASE_DIR / 'static',
   ]
   ```

2. Ensure that `eventhub/urls.py` is properly configured to serve static files:
   ```python
   if settings.DEBUG:
       urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
       urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
   ```

### Database Issues

If the application shows database errors:

1. Delete the `db.sqlite3` file (if it exists)
2. Run migrations again:
   ```
   python manage.py makemigrations
   python manage.py migrate
   ```

## Development Tips

1. **Code Changes**: Any changes you make to the code will be automatically reloaded due to Gunicorn's `--reload` flag

2. **Template Modifications**: Django's template changes should be visible immediately (refresh the page)

3. **Database Exploration**: To explore the database directly, you can use the SQLite shell:
   ```
   python manage.py dbshell
   ```
   
   Or use the Django shell for model-based queries:
   ```
   python manage.py shell
   ```

4. **Admin Interface**: Access the Django admin interface at `/admin` if you've created a superuser

## Deployment

To deploy your EventHub application outside of Replit:

1. Click the "Deploy" button in the Replit interface
2. Follow the prompts to configure your deployment
3. Your application will be available at your Replit subdomain

## Getting Help

If you encounter issues running EventHub on Replit:

1. Check the console output for error messages
2. Review Django's debug page for detailed error information
3. Consult the Django documentation at https://docs.djangoproject.com/