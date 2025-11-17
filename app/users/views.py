from flask import request, redirect, url_for, render_template
from markupsafe import escape
from . import users_bp

@users_bp.route("/hi/<string:name>")
def greetings(name):
    age = request.args.get("age", None, type=int)
    return render_template("users/hi.html",
                           title="Привітання",
                           name=escape(name),
                           age=age)

@users_bp.route("/admin")
def admin():
    to_url = url_for("users.greetings", name="administrator", age=45, external=True)
    print(f"Redirecting to: {to_url}")
    return redirect(to_url)
