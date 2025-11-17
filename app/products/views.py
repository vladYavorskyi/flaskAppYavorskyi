# app/products/views.py

from flask import render_template
from . import products_bp


# Маршрут для відображення списку всіх продуктів
@products_bp.route('/')  # Буде доступно як /products/
def product_list():
    products = [
        {'id': 1, 'name': 'Ноутбук', 'price': 1200},
        {'id': 2, 'name': 'Смартфон', 'price': 750},
        {'id': 3, 'name': 'Монітор', 'price': 300},
    ]
    return render_template('products/list.html',
                           title='Список продуктів',
                           products=products)


# Маршрут для відображення конкретного продукту
@products_bp.route('/<int:product_id>')  # Буде доступно як /products/1
def product_detail(product_id):
    # Тут має бути логіка отримання продукту з бази даних
    # Для прикладу:
    if product_id == 1:
        product = {'id': 1, 'name': 'Ноутбук X1', 'description': 'Потужний ігровий ноутбук.'}
    elif product_id == 2:
        product = {'id': 2, 'name': 'Смартфон Pro', 'description': 'Флагманський смартфон з 5G.'}
    else:
        # Можна використати abort(404)
        product = {'name': 'Продукт не знайдено', 'description': 'Неіснуючий ID.'}

    return render_template('products/detail.html',
                           title=product['name'],
                           product=product)