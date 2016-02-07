"""Talks forms."""
from wtforms import FieldList, StringField, SelectField, BooleanField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from flask_wtf import Form
from wtforms.validators import Optional, Email
from wtforms_alchemy import model_form_factory, ModelFormField

from pygotham.talks.models import Duration, SpeakerInvite, Talk

__all__ = ('TalkSubmissionForm',)

ModelForm = model_form_factory(Form)


def duration_query_factory():
    """Return available :class:`~pygotha.models.Duration` instances."""
    return Duration.query.filter(Duration.inactive == False)


class SpeakerInviteConfirmForm(Form):
    claim_token = StringField()
    talk_name = StringField()
    confirmed = SelectField('Confirmed', [
        (True, 'Confirmed'),
        (False, 'Declined')
    ])
    recording_release = BooleanField()


class SpeakerInvitesForm(ModelForm):

    """Form for editing :class:`~pygotham.models.SpeakerInvite` instances."""

    class Meta:
        model = SpeakerInvite
        field_args = {
            'invited_email': {
                'label': "Co-Presenter's Email",
                'validators': (Email(),),
            },
        }


class TalkSubmissionForm(ModelForm):

    """Form for editing :class:`~pygotham.models.Talk` instances."""

    class Meta:
        model = Talk
        exclude = ('status', 'type')
        field_args = {
            'name': {'label': 'Title'},
            'description': {
                'label': 'Description',
                'description': (
                    'If your talk is accepted this will be made public. It '
                    'should be one paragraph.'
                ),
            },
            'level': {'label': 'Experience Level'},
            'duration': {'label': 'Duration'},
            'abstract': {
                'label': 'Abstract',
                'description': (
                    'Detailed overview. Will be made public if your talk is '
                    'accepted.'
                ),
            },
            'outline': {
                'label': 'Outline',
                'description': (
                    'Sections and key points of the talk meant to give the '
                    'program committee an overview.'
                ),
            },
            'additional_requirements': {
                'label': 'Additional Notes',
                'description': (
                    "Any other information you'd like the program committee "
                    "to know, e.g., additional context and resources, "
                    "previous speaking experiences, etc. This will not be "
                    "shared publicly."
                ),
            },
            'recording_release': {
                'label': 'Recording Release',
                'validators': (Optional(),),
            },
        }

    duration = QuerySelectField(query_factory=duration_query_factory)

    speaker_invites = FieldList(
        ModelFormField(SpeakerInvitesForm),
        min_entries=1
    )
