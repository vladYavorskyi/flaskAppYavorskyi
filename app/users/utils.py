import os
import secrets
from PIL import Image
from flask import current_app

def save_profile_image(form_image):
    random_hex = secrets.token_hex(8)
    _, file_ext = os.path.splitext(form_image.filename)
    image_filename = random_hex + file_ext

    path = os.path.join(
        current_app.root_path,
        'static/images',
        image_filename
    )

    img = Image.open(form_image)
    img.thumbnail((300, 300))
    img.save(path)

    return image_filename
