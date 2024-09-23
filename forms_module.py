from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email

class ClientForm(FlaskForm):
    name = StringField('Client Name', validators=[DataRequired()])
    submit = SubmitField('Add Client')

class ContactForm(FlaskForm):
    name = StringField('First Name', validators=[DataRequired()])
    surname = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Add Contact')
