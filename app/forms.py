from flask_wtf import FlaskForm
from wtforms import (
    StringField, PasswordField, SubmitField,
    TextAreaField, SelectField, BooleanField

)
from wtforms.validators import DataRequired, Length, Email, Regexp


class LoginForm(FlaskForm):
    username = StringField(
        "Username",
        validators=[DataRequired(), Length(min=3, max=30)]
    )
    password = PasswordField(
        "Password",
        validators=[DataRequired(), Length(min=6)]
    )

    remember = BooleanField("Remember me")
    submit = SubmitField("Sign in")



class ContactForm(FlaskForm):
    name = StringField(
        "Name",
        validators=[DataRequired(), Length(min=4, max=10)]
    )

    email = StringField(
        "Email",
        validators=[DataRequired(), Email()]
    )

    phone = StringField(
        "Phone",
        validators=[
            DataRequired(),
            Regexp(r"^\+380\d{7,9}$", message="Phone must be in format +380XXXXXXXXX")
        ]
    )

    subject = SelectField(
        "Subject",
        choices=[
            ("support", "Technical support"),
            ("buy", "Buy question"),
            ("feedback", "Feedback"),
            ("other", "Other")
        ],
        validators=[DataRequired()]
    )

    message = TextAreaField(
        "Message",
        validators=[DataRequired(), Length(max=500)]
    )

    submit = SubmitField("Send")
