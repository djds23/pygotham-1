"""Talks models."""
from uuid import uuid4

from slugify import slugify
from sqlalchemy import event
from sqlalchemy_utils import ArrowType

from pygotham.core import db
from pygotham.events.query import EventQuery

__all__ = ('Category', 'Duration', 'Speaker', 'Talk')


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


class Speaker(db.Model):

    """Speaker, represents the intent to give a talk"""

    __tablename__ = 'speakers'

    id = db.Column(db.Integer, primary_key=True)

    talk_id = db.Column(
        db.Integer, db.ForeignKey('talks.id'), nullable=False,)
    talk = db.relationship(
        'Talk', backref=db.backref('speakers', lazy='dynamic'),)

    user_id = db.Column(
        db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship(
        'User', backref=db.backref('speakers', lazy='dynamic'))

    primary = db.Column(db.Boolean, nullable=False)
    recording_release = db.Column(db.Boolean, nullable=True)
    confirmed_at = db.Column(ArrowType, nullable=True)
    declined_at = db.Column(ArrowType, nullable=True)

users_talks = db.Table('speakers', Speaker.metadata, autoload=True)


class SpeakerInvite(db.Model):

    """SpeakerInvite, an invite from a user to co present a talk"""

    __tablename__ = 'speaker_invites'

    id = db.Column(db.Integer, primary_key=True)

    talk_id = db.Column(
        db.Integer, db.ForeignKey('talks.id'), nullable=False,
    )
    talk = db.relationship(
        'Talk', backref=db.backref('speaker_invites', lazy='dynamic'),
    )

    claim_token = db.Column(db.String(255), nullable=False)
    invited_email = db.Column(db.String(255), nullable=False)


@event.listens_for(SpeakerInvite, 'before_insert')
def set_claim_token(mapper, connection, target):
    if target.claim_token is None:
        target.claim_token = str(uuid4())


class Talk(db.Model):

    """Talk."""

    __tablename__ = 'talks'
    query_class = EventQuery

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
    type = db.Column(
        db.Enum('talk', 'tutorial', name='type'),
        nullable=False,
    )
    duration_id = db.Column(db.ForeignKey('durations.id'), nullable=False)
    duration = db.relationship('Duration')
    recording_release = db.Column(db.Boolean, nullable=True)

    abstract = db.Column(db.Text)
    additional_requirements = db.Column(db.Text)
    objectives = db.Column(db.Text)
    outline = db.Column(db.Text)
    target_audience = db.Column(db.Text)

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
    users = db.relationship(
        'User',
        secondary=users_talks
    )

    video_url = db.Column(db.String(255))

    def __str__(self):
        """Return a printable representation."""
        return self.name

    @property
    def is_accepted(self):
        """Return whether the instance is accepted."""
        return self.status == 'accepted'

    @property
    def slug(self):
        """Return a slug for the instance."""
        return slugify(self.name, max_length=25)
