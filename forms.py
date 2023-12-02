from wtforms import SubmitField, TextAreaField, StringField, DateField, SelectField
from wtforms.validators import InputRequired, ValidationError, Length, DataRequired
import wtforms.validators as validators
from wtforms.validators import Optional
from flask_wtf import FlaskForm
import datetime
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

class PostGigForm(FlaskForm):
    def validate_end_date(self, field):
        if self.start_date.data and field.data:  # Check if both dates are not None
            if field.data < self.start_date.data:
                raise ValidationError(
                    'End date must not be earlier than start date.')
        elif field.data is None:
            raise ValidationError('End date is required.')
        elif self.start_date.data is None:
            raise ValidationError('Start date must be set before end date.')
        
    title = StringField('Title', validators=[InputRequired(), Length(max=100)])
    start_date = DateField(
        'Start Date',
        validators=[
            validators.optional()],
        format='%Y-%m-%d')
    end_date = DateField(
        'End Date',
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

    def validate_start_date(self, field):
        pass
