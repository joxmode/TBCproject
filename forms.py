from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DateField, RadioField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo

class NewsForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    content = TextAreaField("Content", validators=[DataRequired()])
    submit = SubmitField("Post News")

class RegistrationForm(FlaskForm):
    username = StringField("Full Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField("Confirm Password", validators=[
        DataRequired(), EqualTo('password', message='Passwords must match!')
    ])
    birthday = DateField("Date of Birth", validators=[DataRequired()])
    gender = RadioField("Gender", choices=[("male", "Male"), ("female", "Female")], validators=[DataRequired()])
    submit = SubmitField("Sign Up")

class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Log In")

class DeleteForm(FlaskForm):
    submit = SubmitField('Delete')

class InfoForm(FlaskForm):
    title = StringField("TiTle", validators=[DataRequired()])
    content = TextAreaField("Content", validators=[DataRequired()])
    submit = SubmitField ("Post Info")

class CommentForm(FlaskForm):
    text = TextAreaField("Content", validators=[DataRequired()])
    sumbit = SubmitField('Post Comment')