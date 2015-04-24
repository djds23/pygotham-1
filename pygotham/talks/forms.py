"""Talks forms."""

from flask.ext.wtf import Form
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import Optional
from wtforms_alchemy import model_form_factory

from pygotham.talks.models import Duration, Talk

__all__ = ('TalkSubmissionForm',)

ModelForm = model_form_factory(Form)


def duration_query_factory():
    """Return available :class:`~pygotha.models.Duration` instances."""
    return Duration.query.filter(Duration.inactive == False).all()


class TalkSubmissionForm(ModelForm):

    """Form for editing :class:`~pygotham.models.Talk` instances."""

    class Meta:
        model = Talk
        exclude = ('status',)
        field_args = {
            'name': {'label': 'Title'},
            'description': {
                'label': 'Description',
                'description': (
                    'If your talk is accepted this will be made public. '
                    'Should be one paragraph.'
                ),
            },
            'level': {'label': 'Experience Level'},
            'type': {'label': 'Type'},
            'duration': {'label': 'Duration'},
            'abstract': {
                'label': 'Abstract',
                'description': (
                    'Detailed overview. Will be made public if your talk is '
                    'accepted.'
                ),
            },
            'objectives': {
                'label': 'Objectives',
                'description': (
                    'What do you hope to accomplish with this talk?'
                ),
            },
            'target_audience': {
                'label': 'Target Audience',
                'description': (
                    'Who is the intended audience for your talk? (Be '
                    'specific; "Python programmers" is not a good answer to '
                    'this question.)'
                ),
            },
            'outline': {
                'label': 'Outline',
                'description': (
                    'Sections and key points of the talk meant to give the '
                    'committee an overview.'
                ),
            },
            'additional_requirements': {'label': 'Additional Requirements'},
            'recording_release': {
                'label': 'Recording Release',
                'validators': (Optional(),),
            },
        }

    duration = QuerySelectField(query_factory=duration_query_factory)
