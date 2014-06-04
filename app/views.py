from flask import render_template, flash, request, redirect, url_for, abort
from flask.ext.login import login_user, logout_user, login_required, \
                            current_user
from . import app, db
from .forms import RegistrationForm, LoginForm, EditProfileForm, \
                            ChangePasswordForm, DeleteProfileForm
from .models import Monkey

@app.route('/', methods=['GET', 'POST'])
def index():
    if current_user.is_authenticated():
        return redirect(url_for('monkeys'))

    form = LoginForm()
    if form.validate_on_submit():
        monkey = Monkey.query.filter_by(email=form.email.data).first()
        if monkey is not None and monkey.verify_password(form.password.data):
            login_user(monkey)
            return redirect(request.args.get('next') or url_for('monkeys'))
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

        monkey.save()

        flash('You have successfully registered! You can login now', 'success')
        return redirect(url_for('index'))

    return render_template('register.html', form=form)

@app.route('/monkeys', methods=['GET', 'POST'])
@login_required
def monkeys():
    monkeys = Monkey.query.all()
    return render_template('monkeys.html', monkeys=monkeys)

@app.route('/monkey/<int:id>')
@login_required
def profile(id):
    monkey = Monkey.query.filter_by(id=id).first_or_404()
    return render_template('monkey.html', monkey=monkey)

@app.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    monkey = current_user
    form = EditProfileForm(monkey)
    if request.method == 'POST':
        if form.validate_on_submit():
            form.populate_obj(monkey)
            monkey.save()
            flash('Your profile has been successfully updated', 'success')
    else:    
        form.populate_form()

    return render_template('edit_profile.html', form=form)

@app.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    monkey = current_user
    form = ChangePasswordForm(monkey)
    if form.validate_on_submit():
        monkey.password = form.password.data
        monkey.save()
        flash('Your password has been successfully changed', 'success')

    return render_template('change_password.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have successfully logged out', 'success')
    return redirect(url_for('index'))

@app.route('/add_friend/<int:id>')
@login_required
def add_friend(id):
    friend_monkey = Monkey.query.filter_by(id=id).first_or_404()

    if current_user.id == friend_monkey.id:
        flash('You cannot add your self as a friend', 'error')
        return redirect(url_for('profile', id=id))

    try:
        if request.args.get('best_friend') == 'true':
            current_user.add_best_friend(friend_monkey)
        else:
            current_user.add_friend(friend_monkey)
    except ValueError as e:
        flash(str(e), 'error')
    else:
        flash('Friend was successfully added', 'success')
    
    return redirect(url_for('profile', id=id))

@app.route('/delete_profile', methods=['GET', 'POST'])
@login_required
def delete_profile():

    form = DeleteProfileForm()
    if form.validate_on_submit():
        current_user.delete()
        logout_user()
        flash('Your monkey profile was successfully deleted', 'success')
        redirect(url_for('index'))

    return render_template('delete_profile.html', form=form)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
