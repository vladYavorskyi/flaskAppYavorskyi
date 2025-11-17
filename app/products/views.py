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
    product_map = {
        1: {'id': 1, 'name': 'Ноутбук Hewlett-Packard', 'description': 'Потужний ігровий ноутбук Hewlett-Packard.'},
        2: {'id': 2, 'name': 'Смартфон Iphone Pro', 'description': 'Флагманський смартфон з 5G.'},
        3: {'id': 3, 'name': 'Студійний монітор 4K Ultra', 'description': 'Високоякісний монітор для роботи та ігор.'},
    }
    product = product_map.get(product_id)
    if not product:
        return "Продукт не знайдено", 404

    return render_template('products/detail.html',
                           title=product['name'],
                           product=product)
