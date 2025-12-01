from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length


class PostForm(FlaskForm):
    title = StringField(
        "Заголовок",
        validators=[DataRequired(), Length(min=3, max=120)]
    )

    content = TextAreaField(
        "Вміст",
        validators=[DataRequired(), Length(min=3)]
    )

    submit = SubmitField("Зберегти")
