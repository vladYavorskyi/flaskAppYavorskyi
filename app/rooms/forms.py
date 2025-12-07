

from flask_wtf import FlaskForm
from wtforms import (
    StringField, TextAreaField, IntegerField,
    BooleanField, SubmitField, SelectField
)
from wtforms.validators import DataRequired, Length, NumberRange, Optional


class RoomForm(FlaskForm):
    number = StringField(
        "Room number",
        validators=[DataRequired(), Length(max=10)]
    )

    price = IntegerField(
        "Price per night (USD)",
        validators=[DataRequired(), NumberRange(min=0)]
    )

    capacity = IntegerField(
        "Capacity",
        validators=[DataRequired(), NumberRange(min=1, max=20)]
    )

    description = TextAreaField(
        "Description",
        validators=[Optional(), Length(max=500)]
    )

    type_id = SelectField(
        "Room type",
        coerce=int,
        validators=[DataRequired()]
    )

    is_available = BooleanField("Available", default=True)

    submit = SubmitField("Save")


class RoomSearchForm(FlaskForm):
    q = StringField("Search", validators=[Optional(), Length(max=50)])
    submit = SubmitField("Search")
