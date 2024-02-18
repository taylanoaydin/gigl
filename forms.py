from wtforms import SubmitField, TextAreaField, StringField, DateField, SelectField, HiddenField, DecimalField
from wtforms.validators import InputRequired, ValidationError, Length, DataRequired, NumberRange
from wtforms.validators import Optional, ValidationError
from flask_wtf import FlaskForm
from datetime import datetime
import validators


class ApplyForm(FlaskForm):
    message = TextAreaField(
        'Give them your pitch!', [
            InputRequired(), Length(
                min=1, max=1000)])
    submit = SubmitField('Apply')

class BioEditForm(FlaskForm):
    bio = TextAreaField('Bio', [Length(min=0, max=1000)])
    submit = SubmitField('Save')


class LinkEditForm(FlaskForm):
    def validate_url(form, field):
        if (field.data.startswith('http://') or field.data.startswith('https://')):
            if not validators.url(field.data):
                raise ValidationError('This field must be a valid URL.')
        elif field.data and not validators.url('https://' + field.data):
            raise ValidationError('This field must be a valid URL.')

    link1 = StringField('Link1', validators=[Length(min=0, max=50), validate_url])
    link2 = StringField('Link2', validators=[Length(min=0, max=50), validate_url])
    link3 = StringField('Link3', validators=[Length(min=0, max=50), validate_url])
    link4 = StringField('Link4', validators=[Length(min=0, max=50), validate_url])
    submit = SubmitField('Save')


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
        ('Musician', 'Musician'),
        ('Choreographer', 'Choreographer'),
        ('Stylist', 'Stylist'),
        ('Actor', 'Actor'),
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
        ('Musician', 'Musician'),
        ('Choreographer', 'Choreographer'),
        ('Stylist', 'Stylist'),
        ('Actor', 'Actor'),
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
        if field.errors:
            return
        if field.data is None:
            raise ValidationError(
                'End Date is required'
            )
        elif field.data < datetime.now().date():
            raise ValidationError(
                "End date cannot be in the past"
            )
        elif self.start_date.data and field.data < self.start_date.data:
            raise ValidationError(
                'End date must not be earlier than start date.'
                )
        
    def validate_start_date(self, field):
        if field.errors:
            return
        if field.data is None:
            raise ValidationError(
                'Start Date is required'
            )
        elif field.data < datetime.now().date():
            raise ValidationError(
                'Start date cannot be in the past'
            )
        elif self.end_date.data and field.data > self.end_date.data:
            raise ValidationError(
                'Start date cannot be after the end date'
            )
        
    title = StringField('Title', validators=[InputRequired(), Length(max=46)])
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
    price = DecimalField(
        'Price', validators=[
            InputRequired(), NumberRange(min=0, max=999.99, message='Rate must be between $0 and $999.99')]
    )
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



class EditGigForm(FlaskForm):
    title = StringField('Title', validators=[InputRequired(), Length(max=46)])
    price = DecimalField(
        'Price', validators=[
            InputRequired(), NumberRange(min=0, max=999.99, message='Rate must be between $0 and $999.99')])
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
    submit = SubmitField('Finish Editing')
