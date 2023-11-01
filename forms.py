from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField, HiddenField
from wtforms.validators import InputRequired, ValidationError, Length

class ApplyForm(FlaskForm):
    message = TextAreaField('Give them your pitch!', [InputRequired(), Length(min=1, max=1000)])
    submit = SubmitField('Apply')
    gig_id = HiddenField('Gig ID')  # Add this line to your form class