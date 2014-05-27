from flask import render_template
from . import app
from .forms import RegistrationForm, LoginForm

@app.route('/', methods=['GET', 'POST'])
def index():
    form = LoginForm()
    if form.validate_on_submit():
        pass
    return render_template('index.html',form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        pass
    return render_template('register.html', form=form)
