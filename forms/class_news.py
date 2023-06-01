from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FileField, SubmitField, BooleanField
from wtforms.validators import DataRequired


class NewsClassForm(FlaskForm):
    title = StringField("Заголовок", validators=[DataRequired()])
    content = TextAreaField("Содержание")
    photo = FileField("Фото к новости")
    primary_news = BooleanField("Главная новость", false_values={False, 'false', ''})
    submit = SubmitField("Применить")