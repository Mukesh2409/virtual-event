import os
import secrets
from PIL import Image
from flask import url_for, current_app
import logging

def save_picture(form_picture, output_size=(125, 125)):
    """
    Save the user's profile picture with a random name.
    This function is a placeholder as we're not handling file uploads in this app.
    """
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)
    
    try:
        # Create a thumbnail
        i = Image.open(form_picture)
        i.thumbnail(output_size)
        i.save(picture_path)
    except Exception as e:
        logging.error(f"Error saving picture: {e}")
        return None
    
    return picture_fn
