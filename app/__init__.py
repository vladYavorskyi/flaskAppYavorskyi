from flask import Flask, render_template

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile("../config.py")

    # ---- Імпорт блюпрінтів ----
    from .users import users_bp
    from .products import products_bp

    # ---- Реєстрація блюпрінтів ----
    app.register_blueprint(users_bp)
    app.register_blueprint(products_bp)

    # ---- Головні сторінки ----
    @app.route("/")
    def resume():
        return render_template("resume.html", title="Резюме")

    @app.route("/contacts")
    def contacts():
        return render_template("contacts.html", title="Контакти")

    return app
