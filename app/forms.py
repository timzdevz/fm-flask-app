from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, DateField, SubmitField, \
                    ValidationError
from wtforms.validators import Required, Email, Length, EqualTo
from .models import Monkey

class LoginForm(Form):
    email = StringField('Your email', validators=[Email(), Required()])
    password = PasswordField('Your password', validators=[Required()])
    submit = SubmitField('Submit')

class RegistrationForm(Form):
    name = StringField('What is your name?', validators=[Required()])
    email = StringField('Your email', \
        validators=[Email(), Required()])
    password = PasswordField('Your password', validators=[
        Length(min=6, message='Password must be at least 6 charachter long')])
    password2 = PasswordField('Confirm your password', validators=[
        Required(), EqualTo('password', message='Passwords must match.')])
    birth_date = DateField('Your birth date',\
        description='Use DD/MM/YYYY format', format='%d/%m/%Y')
    submit = SubmitField('Submit')

    def validate_email(self, field):
        if Monkey.query.filter_by(email=field.data).first():
            raise ValidationError('Email has been already registered.')

class EditProfileForm(Form):
    name = StringField('Your name', validators=[Required()])
    birth_date = DateField('Your birth date',\
        description='Use DD/MM/YYYY format', format='%d/%m/%Y')
    submit = SubmitField('Submit')

    def __init__(self, monkey, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.monkey = monkey

    def populate_form(self):
        self.process(obj=self.monkey)

class ChangePasswordForm(Form):
    current_password = PasswordField('Your current password', validators=[Required()])
    password = PasswordField('Your new password', validators=[
        Length(min=6, message='Password must be at least 6 charachter long')])
    password2 = PasswordField('Confirm your new password', validators=[
        Required(), EqualTo('password', message='Passwords must match.')])
    submit = SubmitField('Submit')

    def __init__(self, monkey, *args, **kwargs):
        super(ChangePasswordForm, self).__init__(*args, **kwargs)
        self.monkey = monkey

    def validate_current_password(self, field):
        if not self.monkey.verify_password(field.data):
            raise ValidationError('Incorrect password')
