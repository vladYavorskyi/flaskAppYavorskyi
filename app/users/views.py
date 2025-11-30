from flask import (
    request, redirect, url_for, render_template,
    session, flash, make_response
)
from markupsafe import escape
from . import users_bp
from app.forms import LoginForm

@users_bp.route("/hi/<string:name>")
def greetings(name):
    age = request.args.get("age", None, type=int)
    return render_template(
        "users/hi.html",
        title="Привітання",
        name=escape(name),
        age=age
    )


@users_bp.route("/admin")
def admin():
    to_url = url_for("users.greetings", name="administrator", age=45)
    return redirect(to_url)

@users_bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        remember = form.remember.data

        correct_user = "admin"
        correct_pass = "1234"

        if username != correct_user or password != correct_pass:
            flash("Invalid login or password!", "danger")
            return redirect(url_for("users.login"))

        session["username"] = username
        session["remember"] = remember

        flash(f"Welcome, {username}! Remember: {remember}", "success")
        return redirect(url_for("users.profile"))

    return render_template("users/login.html", title="Login", form=form)

@users_bp.route("/profile")
def profile():
    username = session.get("username")
    if not username:
        flash("Спочатку увійдіть!", "warning")
        return redirect(url_for("users.login"))

    cookies = request.cookies.items()

    return render_template(
        "users/profile.html",
        title="Профіль",
        username=username,
        cookies=cookies
    )


@users_bp.route("/logout")
def logout():
    session.pop("username", None)
    flash("Logged out!", "info")
    return redirect(url_for("users.login"))


@users_bp.route("/add_cookie", methods=["POST"])
def add_cookie():
    key = request.form.get("key")
    value = request.form.get("value")

    resp = make_response(redirect(url_for("users.profile")))
    resp.set_cookie(key, value, max_age=60*60*24)
    flash(f"Cookie '{key}' added!", "success")
    return resp


@users_bp.route("/delete_cookie/<key>")
def delete_cookie(key):
    resp = make_response(redirect(url_for("users.profile")))
    resp.delete_cookie(key)
    flash(f"Cookie '{key}' deleted!", "info")
    return resp


@users_bp.route("/delete_all_cookies")
def delete_all_cookies():
    resp = make_response(redirect(url_for("users.profile")))
    for key in request.cookies:
        resp.delete_cookie(key)
    flash("All cookies deleted!", "info")
    return resp


@users_bp.route("/set_theme/<mode>")
def set_theme(mode):
    if mode not in ("light", "dark"):
        flash("Invalid theme!", "danger")
        return redirect(url_for("users.profile"))

    resp = make_response(redirect(url_for("users.profile")))
    resp.set_cookie("theme", mode, max_age=60*60*24*365)
    flash(f"Theme set: {mode}", "success")
    return resp
