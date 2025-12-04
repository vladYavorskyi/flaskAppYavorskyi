from flask import Flask, render_template, redirect, url_for, flash
from app.forms import ContactForm
from flask_migrate import Migrate
from app.database import db


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile("../config.py")

    db.init_app(app)
    migrate = Migrate(app, db)

    from .users import users_bp
    from .products import products_bp

    app.register_blueprint(users_bp)
    app.register_blueprint(products_bp)

    from .posts import posts_bp
    app.register_blueprint(posts_bp)

    @app.route("/")
    def resume():
        return render_template("resume.html", title="Резюме")

    @app.errorhandler(404)
    def not_found(e):
        return render_template("404.html"), 404

    @app.route("/contacts", methods=["GET", "POST"])
    def contacts():
        form = ContactForm()

        if form.validate_on_submit():
            flash("Your message has been sent!", "success")
            return redirect(url_for("contacts"))

        return render_template("contacts.html", title="Контакти", form=form)

    # ІМПОРТ МОДЕЛЕЙ ПЕРЕД ПОВЕРНЕННЯМ APP
    from app.database import models

    return app
