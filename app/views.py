from flask import render_template, flash, redirect, url_for
from . import app, db
from .forms import RegistrationForm, LoginForm
from .models import Monkey

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
        monkey = Monkey(
            name=form.name.data,
            email=form.email.data,
            password=form.password.data,
            birth_date=form.birth_date.data)

        db.session.add(monkey)
        db.session.commit()     

        flash('You have successfully registered! You can login now', 'success')
        return redirect(url_for('index'))

    return render_template('register.html', form=form)
