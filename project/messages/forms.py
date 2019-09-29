from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length
from flask import request

class MessageForm(FlaskForm):
    recipient_no = StringField("Receiver's Phone Number", validators=[DataRequired(), Length(min=10, max=10)])
    message = TextAreaField('Content', validators=[DataRequired(), Length(max=150)])
    send = SubmitField('Send')

class SearchForm(FlaskForm):
    q = StringField('Search', validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        if 'formdata' not in kwargs:
            kwargs['formdata'] = request.args
        if 'csrf_enabled' not in kwargs:
            kwargs['csrf_enabled'] = False
        super(SearchForm, self).__init__(*args, **kwargs)