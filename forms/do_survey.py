from flask_wtf import FlaskForm
from wtforms import SubmitField, BooleanField


class DoSurvey(FlaskForm):
    content1 = BooleanField("Ответ №1", false_values={False, 'false', ''})
    content2 = BooleanField("Ответ №2", false_values={False, 'false', ''})
    content3 = BooleanField("Ответ №3", false_values={False, 'false', ''})
    content4 = BooleanField("Ответ №4", false_values={False, 'false', ''})
    submit = SubmitField("Применить")