from flask import render_template
from . import app
from .forms import RegistrationForm

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        pass
    return render_template('register.html', form=form)
