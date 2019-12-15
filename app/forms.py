from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class DatasetForm(FlaskForm):
    dataset_name = StringField('Dataset name', validators=[DataRequired()])
    dataset_csv = FileField('file', validators=[
                            FileRequired(),
                            FileAllowed(['csv'], 'CSV files only!')]
                        )

    
