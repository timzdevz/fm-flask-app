from flask import render_template, flash, request, redirect, url_for
from flask.ext.login import login_user, logout_user, login_required, \
                            current_user
from . import app, db
from .forms import RegistrationForm, LoginForm
from .models import Monkey

@app.route('/', methods=['GET', 'POST'])
def index():
    form = LoginForm()
    if form.validate_on_submit():
        monkey = Monkey.query.filter_by(email=form.email.data).first()
        if monkey is not None and monkey.verify_password(form.password.data):
            login_user(monkey)
            flash('Logged in successfully.', 'success')
            return redirect(request.args.get('next') or url_for('index'))
        else:
            flash('Invalid email or password', 'error')

    return render_template('index.html', form=form)

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

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have successfully logged out', 'success')
    return redirect(url_for('index'))
