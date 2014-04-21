"""Talks models."""

from pygotham.core import db

__all__ = 'Category', 'Talk',


class Category(db.Model):

    """Talk category."""

    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    slug = db.Column(db.String(75), unique=True, nullable=False)

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
    duration = db.Column(
        db.Enum('30 minute', '60 minute', '90 minute', 'half-day', 'full-day'),
        name='duration',
        default='60 minute',
        nullable=False,
    )
    talk_type = db.Column(
        db.Enum('presentation', 'hands-on class', name='talk_type'),
        default='presentation',
        nullable=False,
    )
    needs_a_TA = db.Column(db.Boolean, default=False, nullable=False)
    recording_release = db.Column(db.Boolean, nullable=False)

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

    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    category = db.relationship(
        'Category', backref=db.backref('talks', lazy='dynamic'),
    )

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('talks', lazy='dynamic'))

    def __str__(self):
        """Return a printable representation."""
        return self.name
