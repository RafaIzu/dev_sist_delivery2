from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from . import login_manager
from . import db


class Product(db.Model):
    __tablename__ = 'product'
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(150))
    price = db.Column(db.Float)
    description = db.Column(db.String(500))
    players = db.Column(db.Integer)
    age = db.Column(db.Integer)
    theme_id = db.Column(db.Integer, db.ForeignKey('theme.id'))


class Theme(db.Model):
    __tablename__ = 'theme'
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(150))
    product = db.relationship('Product', backref="theme")


class Destiny(db.Model):
    __tablename__ = 'destiny'
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    address = db.Column(db.String(200))
    number = db.Column(db.String(100))
    zipcode = db.Column(db.String(100))
    consumer = db.relationship('Consumer', backref="destiny")


class Consumer(UserMixin, db.Model):
    __tablename__ = 'consumer'
    id = db.Column('id', db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    confirmed = db.Column(db.Boolean, default=False)
    destiny_id = db.Column(db.Integer, db.ForeignKey('destiny.id'))

    @property
    def password(self):
        raise AttributeError('password in not readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id}).decode('utf-8')

    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
            print(">>> Confirmou!<<<")
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True

    def __repr__(self):
        return '<User %r>' % self.username


@login_manager.user_loader
def load_user(user_id):
    return Consumer.query.get(int(user_id))
