"""About PyGotham."""

from flask import Blueprint, render_template

from pygotham.models import AboutPage

__all__ = ('blueprint',)

blueprint = Blueprint('about', __name__, url_prefix='/about')


@blueprint.route('/<slug>')
def rst_content(slug):
    page = AboutPage.query.filter_by(slug=slug, active=True).first_or_404()
    return render_template('about.html', page=page)
