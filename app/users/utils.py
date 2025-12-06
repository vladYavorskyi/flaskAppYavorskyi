from functools import wraps
from flask import session, redirect, url_for, flash


def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if "username" not in session:
            flash("Спочатку увійдіть!", "warning")
            return redirect(url_for("users.login"))
        return f(*args, **kwargs)
    return decorated
