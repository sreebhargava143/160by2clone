from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length

class MessageForm(FlaskForm):
    recipient_no = StringField("Receiver's Phone Number", validators=[DataRequired(), Length(min=10, max=10)])
    message = TextAreaField('Content', validators=[DataRequired(), Length(max=150)])
    send = SubmitField('Send')