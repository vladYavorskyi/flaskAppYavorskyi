from flask import Flask, render_template, redirect, url_for, flash
from flask_migrate import Migrate
from flask_login import LoginManager

from app.forms import ContactForm
from app.database import db, bcrypt
from app.users.models import User
from flask_login import current_user
from datetime import datetime



def create_app():
    app = Flask(__name__)
    app.config.from_pyfile("../config.py")

    db.init_app(app)
    bcrypt.init_app(app)
    migrate = Migrate(app, db)

    login_manager = LoginManager()
    login_manager.login_view = "users.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    @app.before_request
    def update_last_seen():
        if current_user.is_authenticated:
            current_user.last_seen = datetime.utcnow()
            db.session.commit()

    from .users import users_bp
    from .products import products_bp
    from .posts import posts_bp
    from .rooms import rooms_bp

    app.register_blueprint(users_bp)
    app.register_blueprint(products_bp)
    app.register_blueprint(posts_bp)
    app.register_blueprint(rooms_bp, url_prefix="/rooms")

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


    from app.database import models
    return app
