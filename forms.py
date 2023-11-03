from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField, HiddenField
from wtforms.validators import InputRequired, ValidationError, Length

class ApplyForm(FlaskForm):
    message = TextAreaField('Give them your pitch!', [InputRequired(), Length(min=1, max=1000)])
    submit = SubmitField('Apply')

class DeleteGigForm(FlaskForm):
    delete = SubmitField('Delete')
    confirm = SubmitField('Yes')
    cancel = SubmitField('No')