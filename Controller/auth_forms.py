from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, PasswordField, BooleanField
from wtforms.fields.core import SelectField
from wtforms.validators import  DataRequired, ValidationError, Length, Email, EqualTo
from app.Model.models import Class, Major, Student
from flask_login import current_user

def get_major():
    return Major.query.all()

def get_majorlabel(theMajor):
    return theMajor.name

class ClassForm(FlaskForm):
    coursenum = StringField('Course Number',[Length(min=3, max=3)])
    title = StringField('Course Title', validators=[DataRequired()])
    major = QuerySelectField('Majors', query_factory = get_major, get_label = get_majorlabel, allow_black=False)
    submit = SubmitField('Post')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    firstname = StringField('First name', validators=[DataRequired()])
    lastname = StringField('Last name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    address = TextAreaField('Address', [Length(min=0, max=200)])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        student = Student.query.filter_by(username=username.data).first()
        if student is not None:
            raise ValidationError('The username already exists! Please use different username')

    def validate_email(self, email):
        student = Student.query.filter_by(username=email.data).first()
        if student is not None:
            raise ValidationError('This email already exists! Please use different email')       

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


