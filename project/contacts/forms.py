from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, RadioField, SubmitField
from project.models import Contact
from wtforms.validators import DataRequired, Length

class ContactForm(FlaskForm):
    contact_name = StringField("Contact Name", validators=[DataRequired()])
    contact_no = StringField("Enter Mobile No", validators=[DataRequired(), Length(min=10, max=10)])
    gender = RadioField('Gender', choices=[('male','Male'),('female','Female')])
    add_contact = SubmitField("Add Contact")

    def validate_contact_no(self, contact_no):
        number = Contact.query.filter_by(contact_no=contact_no.data, owner_id=current_user.user_id).first()
        if number:
            raise ValidationError("Mobile number already added to contacts list")

