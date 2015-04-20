"""About PyGotham."""

from flask import Blueprint, render_template, url_for

from pygotham.models import AboutPage

__all__ = ('blueprint',)

blueprint = Blueprint('about', __name__, url_prefix='/about')


def get_nav_links():
    """Generates all about page titles and urls for use in the navbar."""
    links = {page.title: url_for('about.rst_content', slug=page.slug) for
             page in AboutPage.query.filter_by(active=True)}
    return {'about': links}


@blueprint.route('/<slug>')
def rst_content(slug):
    """Renders database-backed restructured text content as html pages.

    :param slug: the uniquely identifying slug portion of the url
    """
    page = AboutPage.query.filter_by(slug=slug, active=True).first_or_404()
    return render_template('about.html', page=page)
