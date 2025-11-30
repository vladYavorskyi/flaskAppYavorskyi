from flask import Flask, render_template
from app.forms import ContactForm

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile("../config.py")

    from .users import users_bp
    from .products import products_bp

    app.register_blueprint(users_bp)
    app.register_blueprint(products_bp)

    @app.route("/")
    def resume():
        return render_template("resume.html", title="Резюме")

    @app.route("/contacts", methods=["GET", "POST"])
    def contacts():
        form = ContactForm()

        if form.validate_on_submit():
            flash("Your message has been sent!", "success")
            return redirect(url_for("contacts"))

        return render_template("contacts.html", title="Контакти", form=form)

    return app
