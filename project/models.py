from sqlalchemy.orm import backref
from . import db

class Consumer(db.Model):
    __tablename__ = 'consumer'
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(150))
    email = db.Column(db.String(150))
    password = db.Column(db.String(150))
    destiny_id = db.Column(db.Integer, db.ForeignKey('destiny.id'))

class Product(db.Model):
    __tablename__ = 'product'
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(150))
    price = db.Column(db.Float)
    description = db.Column(db.String(500))
    players = db.Column(db.Integer)
    age = db.Column(db.Integer)

class Destiny(db.Model):
    __tablename__ = 'destiny'
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    address = db.Column(db.String(200))
    number = db.Column(db.String(100))
    zipcode = db.Column(db.String(100))
    consumer = db.relationship('Consumer', backref="destiny")
