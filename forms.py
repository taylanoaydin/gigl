from wtforms import SubmitField, TextAreaField, StringField, DateField, SelectField, HiddenField
from wtforms.validators import InputRequired, ValidationError, Length, DataRequired
import wtforms.validators as validators
from wtforms.validators import Optional
from flask_wtf import FlaskForm
from datetime import datetime
from flask_wtf import Form  # Import Form instead of FlaskForm


class ApplyForm(FlaskForm):
    message = TextAreaField(
        'Give them your pitch!', [
            InputRequired(), Length(
                min=1, max=1000)])
    submit = SubmitField('Apply')

class BioEditForm(FlaskForm):
    bio = TextAreaField('Bio', [Length(min=0, max=1000)])
    submit = SubmitField('Submit')


class LinkEditForm(FlaskForm):
    link1 = StringField('Link1', [Length(min=0, max=50)])
    link2 = StringField('Link2', [Length(min=0, max=50)])
    link3 = StringField('Link3', [Length(min=0, max=50)])
    link4 = StringField('Link4', [Length(min=0, max=50)])
    submit = SubmitField('Submit')


class DeleteGigForm(FlaskForm):
    delete = SubmitField('Delete')
    confirm = SubmitField('Yes', render_kw={'id': 'confirmButton'})
    cancel = SubmitField('No', render_kw={'id': 'cancelButton'})


class SearchForm(FlaskForm):
    keyword = StringField('Keyword', validators=[Optional()])
    category = SelectField('Category', choices=[
        ('', 'Any Category'),
        ('teaching', 'Teaching'),
        ('research', 'Research'),
        ('technical', 'Technical'),
        ('writing', 'Writing'),
        ('graphic_design', 'Graphic Design'),
        ('photography_film', 'Photography/Film'),
        ('events', 'Events'),
        ('marketing', 'Marketing'),
        ('administrative', 'Administrative'),
        ('volunteer', 'Volunteer'),
        ('fitness', 'Fitness'),
        ('other', 'Other')
    ])
    submit = SubmitField('Search')


class ProfileSearchForm(FlaskForm):
    keyword = StringField('Keyword', validators=[Optional()])
    specialty = SelectField('Specialty', choices=[
        ('', 'Any Specialty'),
        ('Tutor', 'Tutor'),
        ('Researcher', 'Researcher'),
        ('Developer', 'Developer'),
        ('Writer', 'Writer'),
        ('Graphic Designer', 'Graphic Designer'),
        ('Photographer', 'Photographer'),
        ('Volunteer', 'Volunteer'),
        ('Fitness Coach', 'Fitness Coach'),
        ('Cosmetician', 'Cosmetician'),
        ('Cook', 'Cook'),
        ('Fashion Designer', 'Fashion Designer'),
        ('Miscellaneous', 'Miscellaneous')
    ])
    submit = SubmitField('Search')

class SpecialtySelectForm(FlaskForm):
    specialty = SelectField('Specialty', choices=[
        ('Not Chosen', 'Not Chosen'),
        ('Tutor', 'Tutor'),
        ('Researcher', 'Researcher'),
        ('Developer', 'Developer'),
        ('Writer', 'Writer'),
        ('Graphic Designer', 'Graphic Designer'),
        ('Photographer', 'Photographer'),
        ('Volunteer', 'Volunteer'),
        ('Fitness Coach', 'Fitness Coach'),
        ('Cosmetician', 'Cosmetician'),
        ('Cook', 'Cook'),
        ('Fashion Designer', 'Fashion Designer'),
        ('Miscellaneous', 'Miscellaneous')
    ])
    submit = SubmitField('Choose')

class SetStatusForm(FlaskForm):
    applicantID = HiddenField('AppID')
    gigID = HiddenField('GigID')
    status = SelectField('Status', choices=[
        ('YES', 'Accepted'),
        ('UNDECIDED', 'Pending'),
        ('NO', 'Rejected')
    ])

class PostGigForm(FlaskForm):
    def validate_end_date(self, field):
        if field.data is None:
            raise ValidationError(
                'End Date is required'
            )
        elif field.data < datetime.now().date():
            raise ValidationError(
                "End date cannot be in the past"
            )
        if field.data < self.start_date.data:
            raise ValidationError(
                'End date must not be earlier than start date.'
                )
        
    def validate_start_date(self, field):
        if field.data is None:
            raise ValidationError(
                'Start Date is required'
            )
        elif field.data < datetime.now().date():
            raise ValidationError(
                'Start date cannot be in the past'
            )
        if field.data > self.end_date.data:
            raise ValidationError(
                'Start date cannot be after the end date'
            )
        
    title = StringField('Title', validators=[InputRequired(), Length(max=100)])
    start_date = DateField(
        'Start Date',
        validators=[
            validate_start_date
            ],
        format='%Y-%m-%d')
    end_date = DateField(
        'End Date',
        validators=[
            validate_end_date
        ],
        format='%Y-%m-%d')
    qualifications = TextAreaField(
        'Qualifications', validators=[
            InputRequired(), Length(
                max=500)])
    description = TextAreaField(
        'Description', validators=[
            InputRequired(), Length(
                max=1000)])
    categories = SelectField(
        'Categories',
        validators=[
            DataRequired(
                message='Select A Category'),
            InputRequired()],
        choices=[
            ('',
             'Select A Category'),
            ('teaching',
             'Teaching'),
            ('research',
             'Research'),
            ('technical',
             'Technical'),
            ('writing',
             'Writing'),
            ('graphic_design',
             'Graphic Design'),
            ('photography_film',
             'Photography/Film'),
            ('events',
             'Events'),
            ('marketing',
             "Marketing"),
            ('administrative',
             "Administrative"),
            ('volunteer',
             "Volunteer"),
            ('fitness',
             'Fitness'),
            ('other',
             'Other')])
    submit = SubmitField('Submit')
