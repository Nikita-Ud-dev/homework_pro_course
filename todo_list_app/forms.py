from flask_wtf import FlaskForm
from wtforms import StringField, DateTimeLocalField, TextAreaField
from wtforms.validators import DataRequired, Length

class TaskForm(FlaskForm):
    title = StringField("Назва завдання", validators=[DataRequired() , Length(max=40)])
    description = TextAreaField("Опис завдання", validators=[Length(max=500)])
    date_limit = DateTimeLocalField("Дата: до якого потрібно здати", format="%Y-%m-%dT%H:%M", validators=[DataRequired()])