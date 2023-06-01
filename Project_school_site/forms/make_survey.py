from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired


class MakeSurvey(FlaskForm):
    title = StringField("Заголовок", validators=[DataRequired()])
    question = TextAreaField("Вопрос")
    content1 = TextAreaField("Ответ №1")
    content2 = TextAreaField("Ответ №2")
    content3 = TextAreaField("Ответ №3")
    content4 = TextAreaField("Ответ №4")
    submit = SubmitField("Применить")