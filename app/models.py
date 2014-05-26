from . import db

class Monkey(db.Model):
    __tablename__ = 'monkeys'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    email = db.Column(db.String(64), unique=True)
    age = db.Column(db.Date())

    def __repr__(self):
        return '<User {} {}>'.format(self.id, self.email)