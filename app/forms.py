from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, DateField, SubmitField
from wtforms.validators import Required, Email, Length

class RegistrationForm(Form):
    name = StringField('What is your name?', validators=[Required()])
    email = StringField('Your email', \
        validators=[Email(), Required()])
    password = PasswordField('Your password', validators=[Length(min=6, \
            message='Your password must at least 6 char. long')])
    birth_date = DateField('Your birth date',\
        description='Use DD/MM/YYYY format', format='%d/%m/%Y')
    submit = SubmitField('Submit')
