"""About package."""

from flask import url_for

from pygotham.about.models import AboutPage

__all__ = ('get_about_links',)

def get_about_links():
    """Get a list of About Page names and hrefs."""
    return ((page.title, url_for('about.rst_content', slug=page.slug)) for page 
            in AboutPage.query.filter_by(active=True).order_by(AboutPage.title))
