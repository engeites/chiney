from datetime import datetime

from flask_login import UserMixin

from app import db
from app import login_manager


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(100), unique=False, nullable=False)
    posts = db.relationship('Text', backref='author', lazy=True)
    posts_quantity = db.Column(db.Integer, default=0)

    def __init__(self, username, password):
        self.username = username
        self.password = password


class Text(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    header = db.Column(db.String(120), nullable=False, unique=True)
    text = db.Column(db.Text, nullable=False)
    translation = db.Column(db.Text, nullable=False)
    description = db.Column(db.String(120), default=f"Учебный текст#{id}")
    date = db.Column(db.DateTime, default=datetime.utcnow())
    approved = db.Column(db.Boolean, default=False)
    likes = db.Column(db.Integer, default=0, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    level = db.Column(db.Integer, nullable=False)

    def __init__(self, header, text, translation, level, user_id):
        self.header = header
        self.text = text
        self.translation = translation
        self.level = level
        self.user_id = user_id


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


db.create_all()
