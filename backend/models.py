from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime




db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user_data'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    hpsw = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Integer, default=0)
    time = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.hpsw = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hpsw, password)


class Event(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    event_name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    start_datetime = db.Column(db.DateTime, nullable=False)
    end_datetime = db.Column(db.DateTime, nullable=False)
    location = db.Column(db.Text)
    event_type = db.Column(db.String(50), nullable=False)
    participant_limit = db.Column(db.Integer)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_cancelled = db.Column(db.Boolean, default=False)

    category = db.relationship('Category', backref='events')
    tags = db.relationship('Tag', secondary='event_tags', backref='events')
    files = db.relationship('EventFile', backref='event')

class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)

class Tag(db.Model):
    __tablename__ = 'tags'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)

class EventTag(db.Model):
    __tablename__ = 'event_tags'
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key=True)

class EventFile(db.Model):
    __tablename__ = 'event_files'
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))
    file_name = db.Column(db.String(255), nullable=False)
    file_data = db.Column(db.Text)
    file_type = db.Column(db.String(50), nullable=False)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)

class EventParticipant(db.Model):
    __tablename__ = 'event_participants'
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id', ondelete='CASCADE'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user_data.id', ondelete='CASCADE'), nullable=False)
    registration_time = db.Column(db.DateTime, default=datetime.utcnow)

    event = db.relationship('Event', backref='participants')
    user = db.relationship('User', backref='registered_events')

class EventWaitlist(db.Model):
    __tablename__ = 'event_waitlist'
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id', ondelete='CASCADE'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user_data.id', ondelete='CASCADE'), nullable=False)
    registration_time = db.Column(db.DateTime, default=datetime.utcnow)

    event = db.relationship('Event', backref='waitlist')
    user = db.relationship('User', backref='waitlist_events')