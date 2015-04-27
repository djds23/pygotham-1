"""Talks models."""
from sqlalchemy.dialects.postgresql import JSON

from pygotham.core import db

__all__ = ('Category', 'Duration', 'Talk')


class Category(db.Model):

    """Talk category."""

    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    slug = db.Column(db.String(75), unique=True, nullable=False)

    def __str__(self):
        """Return a printable representation."""
        return self.name


class Duration(db.Model):

    """Talk duration."""

    __tablename__ = 'durations'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    inactive = db.Column(db.Boolean, default=False)

    __mapper_args__ = {
        'order_by': (inactive, duration),
    }

    def __str__(self):
        """Return a printable representation."""
        return self.name


class Talk(db.Model):

    """Talk."""

    __tablename__ = 'talks'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    status = db.Column(
        db.Enum('draft', 'submitted', 'accepted', 'rejected', name='status'),
        default='draft',
        nullable=False,
    )
    level = db.Column(
        db.Enum('novice', 'intermediate', 'advanced', name='level'),
        nullable=False,
    )
    duration_id = db.Column(db.ForeignKey('durations.id'), nullable=False)
    duration = db.relationship('Duration')
    recording_release = db.Column(db.Boolean, nullable=True)

    additional_requirements = db.Column(db.Text)

    event_id = db.Column(
        db.Integer, db.ForeignKey('events.id'), nullable=False,
    )
    event = db.relationship(
        'Event', backref=db.backref('talks', lazy='dynamic'),
    )

    category_id = db.Column(
        db.Integer, db.ForeignKey('categories.id'), nullable=True)
    category = db.relationship(
        'Category', backref=db.backref('talks', lazy='dynamic'),
    )

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('talks', lazy='dynamic'))

    video_url = db.Column(db.String(255))

    def __str__(self):
        """Return a printable representation."""
        return self.name

    @property
    def is_accepted(self):
        """Return whether the instance is accepted."""
        return self.status == 'accepted'


class CoPresenter(db.Model):

    __tablename__ = 'copresenters'

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(255), info={'label': 'Name'}, nullable=True)
    email = db.Column(db.String(255), nullable=True)
    twitter_handle = db.Column(db.String(255), nullable=True)

    talk_id = db.Column(db.Integer, db.ForeignKey('talks.id'), nullable=False)
    talk = db.relationship('Talk', backref=db.backref('co_presenters', lazy='dynamic'))