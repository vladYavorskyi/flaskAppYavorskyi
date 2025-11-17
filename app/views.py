# app/views.py

from flask import render_template
from app import app

@app.route("/")
def home():
    return render_template("resume.html", title="Резюме")

@app.route("/resume")
def resume():
    return render_template("resume.html", title="Резюме")

@app.route("/contacts")
def contacts():
    return render_template("contacts.html", title="Контакти")
