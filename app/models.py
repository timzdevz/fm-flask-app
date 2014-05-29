from werkzeug.security import generate_password_hash, check_password_hash
from flask.ext.login import UserMixin
from . import db, login_manager
from datetime import date, timedelta

ONE_YEAR_SEC = timedelta(days=365).total_seconds()

class Monkey(UserMixin, db.Model):
    __tablename__ = 'monkeys'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    email = db.Column(db.String(64), unique=True)
    password_hash = db.Column(db.String(128))
    birth_date = db.Column(db.Date())

    @property
    def age(self):
        return int((date.today() - self.birth_date).total_seconds() // ONE_YEAR_SEC)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute') 

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {} {}>'.format(self.id, self.email)

@login_manager.user_loader
def load_user(user_id):
    return Monkey.query.get(int(user_id))
