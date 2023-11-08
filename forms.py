from wtforms import SubmitField, TextAreaField, StringField, DateField, SelectField
from wtforms.validators import InputRequired, ValidationError, Length, DataRequired
import wtforms.validators as validators
from wtforms.validators import Optional
from flask_wtf import FlaskForm
from flask_wtf import Form  # Import Form instead of FlaskForm


class ApplyForm(FlaskForm):
    message = TextAreaField('Give them your pitch!', [InputRequired(), Length(min=1, max=1000)])
    submit = SubmitField('Apply')

class DeleteGigForm(FlaskForm):
    delete = SubmitField('Delete')
    confirm = SubmitField('Yes')
    cancel = SubmitField('No')

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


class PostGigForm(FlaskForm):
    title = StringField('Title', validators=[InputRequired(), Length(max=50)])
    start_date = DateField('Start Date', validators=[validators.optional()], format='%Y-%m-%d')
    end_date = DateField('End Date', validators=[validators.optional()], format='%Y-%m-%d')
    qualifications = TextAreaField('Qualifications', validators=[InputRequired(), Length(max=900, message='')])
    description = TextAreaField('Description', validators=[InputRequired(), Length(max=1200, message='')])
    categories = SelectField('Categories', validators=[DataRequired(message='Select A Category'),InputRequired()],
                             choices=[('', 'Select A Category'),
                                      ('teaching', 'Teaching'),
                                      ('research', 'Research'),
                                      ('technical', 'Technical'),
                                      ('writing', 'Writing'),
                                      ('graphic_design', 'Graphic Design'),
                                      ('photography_film', 'Photography/Film'),
                                      ('events', 'Events'),
                                      ('marketing', "Marketing"),
                                      ('administrative', "Administrative"),
                                      ('volunteer', "Volunteer"),
                                      ('fitness', 'Fitness'),
                                      ('other', 'Other')])
    submit = SubmitField('Submit')

    def validate_end_date(self, field):
        if self.start_date.data and field.data:  # Check if both dates are not None
            if field.data < self.start_date.data:
                raise ValidationError('End date must not be earlier than start date.')
        elif field.data is None:
            raise ValidationError('End date is required.')
        elif self.start_date.data is None:
            raise ValidationError('Start date must be set before end date.')
