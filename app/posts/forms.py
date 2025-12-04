from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length
from wtforms import SelectMultipleField




class PostForm(FlaskForm):
    title = StringField(
        "Заголовок",
        validators=[DataRequired(), Length(min=3, max=120)]
    )

    content = TextAreaField(
        "Вміст",
        validators=[DataRequired(), Length(min=3)]
    )

    tags = SelectMultipleField(
        "Теги",
        coerce=int
    )

    user_id = SelectField(
        "Автор",
        coerce=int,
        validators=[DataRequired()]
    )

    submit = SubmitField("Зберегти")
