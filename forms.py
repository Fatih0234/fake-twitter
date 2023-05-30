from wtforms import StringField, PasswordField, BooleanField, TextAreaField
from wtforms.validators import InputRequired, Length
from flask_wtf.file import FileField, FileAllowed
from flask_uploads import UploadSet, IMAGES, configure_uploads
from flask_wtf import FlaskForm


class RegisterForm(FlaskForm):
    name = StringField('Full name', validators=[InputRequired("A full name is required"), Length(min=4, max=100, message="Your name should be between 4 and 100 characters long")])
    username = StringField('Username', validators=[InputRequired("Username is required"), Length(min=4, max=30, message="Your username should be between 4 and 30 characters long")])
    password = PasswordField('Password', validators=[InputRequired("Password is required"), Length(min=4, max=30)])
    image = FileField(validators=[FileAllowed(IMAGES, 'Only images are accepted')])

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired("Username is required"), Length(min=4, max=30, message="Your username should be between 4 and 30 characters long")])
    password = PasswordField('Password', validators=[InputRequired("Password is required"), Length(min=4, max=30)])
    remember = BooleanField('Remember me')

class TweetForm(FlaskForm):
    text = TextAreaField('What\'s happening?', validators=[InputRequired("Tweet can't be empty"), Length(min=1, max=140, message="Your tweet should be between 1 and 140 characters long")])
