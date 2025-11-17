# app/products/__init__.py
from flask import Blueprint

products_bp = Blueprint(
    'products',
    __name__,
    template_folder='templates',
    url_prefix='/products'
)

# Імпортуємо views, щоб маршрути додалися до blueprint
from app.products import views
