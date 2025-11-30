

from flask import render_template
from . import products_bp


@products_bp.route('/')
def product_list():
    products = [
        {'id': 1, 'name': 'Ноутбук', 'price': 1200},
        {'id': 2, 'name': 'Смартфон', 'price': 750},
        {'id': 3, 'name': 'Монітор', 'price': 300},
    ]
    return render_template('products/list.html',
                           title='Список продуктів',
                           products=products)


@products_bp.route('/<int:product_id>')
def product_detail(product_id):

    if product_id == 1:
        product = {'id': 1, 'name': 'Ноутбук X1', 'description': 'Потужний ігровий ноутбук.'}
    elif product_id == 2:
        product = {'id': 2, 'name': 'Смартфон Pro', 'description': 'Флагманський смартфон з 5G.'}
    else:
        product = {'name': 'Продукт не знайдено', 'description': 'Неіснуючий ID.'}

    return render_template('products/detail.html',
                           title=product['name'],
                           product=product)