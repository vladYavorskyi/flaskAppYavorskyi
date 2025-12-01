from flask import render_template, abort
from . import products_bp
from app.database.models import Product


@products_bp.route("/")
def product_list():
    products = Product.query.all()
    return render_template("products/list.html",
                           title="Список продуктів",
                           products=products)


@products_bp.route("/<int:product_id>")
def product_detail(product_id):
    product = Product.query.get(product_id)

    if product is None:
        abort(404)

    return render_template("products/detail.html",
                           title=product.name,
                           product=product)
