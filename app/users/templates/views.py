from flask import render_template, redirect
from . import users_bp

@users_bp.route('/hi/<name>')
def greetings(name):
    return render_template('greetings.html', name=name, age=None)

@users_bp.route('/admin')
def admin():
    return redirect('/hi/admin')
