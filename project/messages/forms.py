from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError
from flask import request
from project. models import Contact
from sqlalchemy import and_
from flask_login import current_user


class MessageForm(FlaskForm):
    recipient_no = StringField("Receiver's Phone Number", validators=[DataRequired(), Length(min=10, max=10)])
    message = TextAreaField('Content', validators=[DataRequired(), Length(max=150)])
    send = SubmitField('Send')

    def validate_recipient_no(self, recipient_no):
        recipient = Contact.query.filter(and_(Contact.owner == current_user, Contact.contact_no == recipient_no.data)).first()
        print ("#"*20,recipient,"#"*20)
        if recipient is None:
            raise ValidationError("Add the recipient to contacts to send messages for security reasons")

class SearchForm(FlaskForm):
    q = StringField('Search', validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        if 'formdata' not in kwargs:
            kwargs['formdata'] = request.args
        if 'csrf_enabled' not in kwargs:
            kwargs['csrf_enabled'] = False
        super(SearchForm, self).__init__(*args, **kwargs)