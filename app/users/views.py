from flask import (
    request, redirect, url_for, render_template,
    flash, make_response
)
from markupsafe import escape
from . import users_bp
from app.forms import LoginForm
from app.users.forms import RegistrationForm, EditProfileForm
from app.database import db
from app.users.models import User
from flask_login import login_user, logout_user, login_required, current_user
from app.users.utils import save_profile_image


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


@users_bp.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data
        )
        user.set_password(form.password.data)

        db.session.add(user)
        db.session.commit()

        flash("Account created successfully!", "success")
        return redirect(url_for("users.login"))

    return render_template("users/register.html", form=form)


@users_bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if not user or not user.check_password(form.password.data):
            flash("Invalid login or password!", "danger")
            return redirect(url_for("users.login"))

        login_user(user)
        flash(f"Welcome, {user.username}!", "success")
        return redirect(url_for("users.profile"))

    return render_template("users/login.html", title="Login", form=form)


@users_bp.route("/profile")
@login_required
def profile():
    cookies = request.cookies.items()
    return render_template("users/profile.html", cookies=cookies)


@users_bp.route("/edit_profile", methods=["GET", "POST"])
@login_required
def edit_profile():
    form = EditProfileForm()

    if form.validate_on_submit():


        if form.image.data:
            image_file = save_profile_image(form.image.data)
            current_user.image = image_file

        current_user.username = form.username.data
        current_user.about_me = form.about_me.data

        db.session.commit()

        flash("Profile updated successfully!", "success")
        return redirect(url_for("users.profile"))


    form.username.data = current_user.username
    form.about_me.data = current_user.about_me

    return render_template("users/edit_profile.html", form=form)

@users_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out!", "info")
    return redirect(url_for("users.login"))

@users_bp.route("/add_cookie", methods=["POST"])
@login_required
def add_cookie():
    key = request.form.get("key")
    value = request.form.get("value")

    resp = make_response(redirect(url_for("users.profile")))
    resp.set_cookie(key, value, max_age=60 * 60 * 24)
    flash(f"Cookie '{key}' added!", "success")
    return resp


@users_bp.route("/delete_cookie/<key>")
@login_required
def delete_cookie(key):
    resp = make_response(redirect(url_for("users.profile")))
    resp.delete_cookie(key)
    flash(f"Cookie '{key}' deleted!", "info")
    return resp


@users_bp.route("/delete_all_cookies")
@login_required
def delete_all_cookies():
    resp = make_response(redirect(url_for("users.profile")))
    for key in request.cookies:
        resp.delete_cookie(key)
    flash("All cookies deleted!", "info")
    return resp


@users_bp.route("/set_theme/<mode>")
@login_required
def set_theme(mode):
    if mode not in ("light", "dark"):
        flash("Invalid theme!", "danger")
        return redirect(url_for("users.profile"))

    resp = make_response(redirect(url_for("users.profile")))
    resp.set_cookie("theme", mode, max_age=60 * 60 * 24 * 365)
    flash(f"Theme set: {mode}", "success")
    return resp
