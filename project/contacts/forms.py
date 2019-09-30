from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, RadioField, SubmitField
from project.models import Contact
from wtforms.validators import DataRequired, Length, ValidationError
from flask import request

class ContactForm(FlaskForm):
    contact_name = StringField("Contact Name", validators=[DataRequired()])
    contact_no = StringField("Enter Mobile No", validators=[DataRequired(), Length(min=10, max=10)])
    gender = RadioField('Gender', choices=[('male','Male'),('female','Female')], validators=[DataRequired()])
    add_contact = SubmitField("Add Contact")
    delete_contact = SubmitField("Delete Contact")

    def validate_contact_no(self, contact_no):

        print(request.form.get)
        if request.form.get('add_contact'):
            number = Contact.query.filter_by(contact_no=contact_no.data, owner_id=current_user.id).first()
            if number:
                raise ValidationError("Mobile number already added to contacts list")

