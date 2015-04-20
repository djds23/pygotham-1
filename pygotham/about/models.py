"""About models."""

from slugify import slugify
from sqlalchemy_utils.decorators import generates

from pygotham.core import db

__all__ = ('AboutPage',)


class AboutPage(db.Model):
    """About page."""

    __tablename__ = 'about_pages'

    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(255), nullable=False, unique=True)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    active = db.Column(db.Boolean, nullable=False)

    def __str__(self):
        """Return a printable representation."""
        return self.title

    @generates(slug)
    def _create_slug(self):
        """Return the slug for the announcement."""
        return slugify(self.title)
