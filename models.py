from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    decks = db.relationship('Deck', backref='author', lazy=True)


class Deck(db.Model):
    __tablename__ = 'decks'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    is_public = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    cards = db.relationship('Card', backref='deck', lazy=True, cascade="all, delete-orphan")


class Card(db.Model):
    __tablename__ = 'cards'
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.Text, nullable=False)
    answer = db.Column(db.Text, nullable=False)
    image_path = db.Column(db.String(255))
    deck_id = db.Column(db.Integer, db.ForeignKey('decks.id'), nullable=False)

    def __repr__(self):
        return f'<Card {self.id} in Deck {self.deck_id}>'
