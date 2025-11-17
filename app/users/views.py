# app/users/views.py

from flask import request, redirect, url_for, render_template
from markupsafe import escape
from . import users_bp  # Імпортуємо наш Blueprint


@users_bp.route("/hi/<string:name>")  # Буде доступно як /users/hi/<name>
def greetings(name):
    # Отримуємо параметр age з GET-запиту, None за замовчуванням, приводимо до int
    age = request.args.get("age", None, type=int)

    # render_template шукає шаблон у app/users/templates/users/hi.html
    return render_template("users/hi.html",
                           title="Привітання",
                           name=escape(name),
                           age=age)


@users_bp.route("/admin")  # Буде доступно як /users/admin
def admin():
    # url_for використовує назву Blueprint: 'users.greetings'
    to_url = url_for("users.greetings", name="administrator", age=45, external=True)
    print(f"Redirecting to: {to_url}")
    return redirect(to_url)