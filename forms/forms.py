from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from flask_wtf.file import FileAllowed
from wtforms.validators import DataRequired

class UploadImageForm(FlaskForm):
    picture = FileField('Image to analyze', validators=[DataRequired(), FileAllowed(['jpg'])])
    submit = SubmitField('Analyse')