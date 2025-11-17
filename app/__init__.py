from flask import Flask, render_template

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile("../config.py")  # або просто 'config.py', якщо в корені

    from .users import users_bp
    from .products import products_bp

    app.register_blueprint(users_bp)
    app.register_blueprint(products_bp)

    @app.route("/")
    @app.route("/resume")
    def resume():
        return render_template("resume.html", title="Резюме")

    @app.route("/contacts")
    def contacts():
        return render_template("contacts.html", title="Контакти")

    return app
