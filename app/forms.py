from flask_wtf import FlaskForm #type:ignore
from wtforms import StringField, SubmitField #type:ignore
from wtforms.validators import DataRequired, Length #type:ignore 

class TaskForm(FlaskForm):
    task = StringField("New Task:", validators = [Length(max=200), DataRequired()])
    description = StringField("Describe the task:", validators = [Length(max=2000)])
    submit = SubmitField("Submit")