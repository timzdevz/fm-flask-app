from werkzeug.security import generate_password_hash, check_password_hash
from flask.ext.login import UserMixin
from . import db, login_manager
from datetime import date, timedelta

ONE_YEAR_SEC = timedelta(days=365).total_seconds()

class Friendship(db.Model):
    __tablename__ = 'friendships'
    monkey_1 = db.Column(db.Integer,\
        db.ForeignKey('monkeys.id'), primary_key=True)
    monkey_2 = db.Column(db.Integer, \
        db.ForeignKey('monkeys.id'), primary_key=True)

class Monkey(UserMixin, db.Model):
    __tablename__ = 'monkeys'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    email = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    birth_date = db.Column(db.Date())
    best_friend_id = db.Column(db.Integer)

    friended = db.relationship('Monkey',
                                secondary=Friendship.__tablename__,
                                primaryjoin=Friendship.monkey_1 == id,
                                secondaryjoin=Friendship.monkey_2 == id,
                                backref=db.backref('friends', lazy='dynamic'),
                                lazy='dynamic')
    @property
    def friends_total(self):
        return self.friends.count() + self.friended.count()

    @property
    def best_friend(self):
        if self.has_best_friend():
            return Monkey.query.get(self.best_friend_id)
    
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

    def add_friend(self, monkey_friend):
        if self.has_friend(monkey_friend):
            raise ValueError('Cannot add friend: friend already exists')

        self.friends.append(monkey_friend)
        self.save()

    def add_best_friend(self, monkey_friend):
        if self.has_best_friend():
            raise ValueError('Cannot add best friend: best friend already exists')

        if not self.has_friend(monkey_friend):
            raise ValueError('First you have to add monkey as friend')

        self.best_friend_id = monkey_friend.id
        self.save()

    def delete_friend(self, monkey_friend):
        if monkey_friend in self.friends:
            self.friends.remove(monkey_friend)
        if monkey_friend in self.friended:
            self.friended.remove(monkey_friend)

        if self.best_friend_id == monkey_friend.id:
            self.best_friend_id = None

        self.save()

    def has_friend(self, monkey_friend):
        return monkey_friend in (self.friends.filter_by(id=monkey_friend.id).first(), \
                                self.friended.filter_by(id=monkey_friend.id).first())

    def has_best_friend(self):
        return self.best_friend_id is not None

    def is_best_friend(self, monkey_friend):
        return monkey_friend.id == self.best_friend_id

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return '<Monkey {} {}>'.format(self.id, self.email)

@login_manager.user_loader
def load_user(user_id):
    return Monkey.query.get(int(user_id))
