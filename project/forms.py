from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, RadioField, TextAreaField
from project.models import User, Contact
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user

class LoginForm(FlaskForm):
    mobile_no = StringField("Mobile No", validators=[DataRequired(), Length(min=10, max=10)])
    password = PasswordField("Password", validators=[DataRequired()])
    login = SubmitField("Login")

class SignUpForm(FlaskForm):
    username = StringField("Name", validators=[DataRequired()])
    mobile_no = StringField("Mobile No", validators=[DataRequired(), Length(min=10, max=10)])
    email_id = StringField("Email", validators=[DataRequired(), Email()])
    gender = RadioField('Gender', choices=[('male','Male'),('female','Female')])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo("password")])
    sign_up = SubmitField("Sign Up")
    
    def validate_mobile_no(self, mobile_no):
        number = User.query.filter_by(mobile_no=mobile_no.data).first()
        if number:
            raise ValidationError("Mobile number already registered with us")
    def validate_email_id(self, email_id):
        email = User.query.filter_by(email_id=email_id.data).first()
        if email:
            raise ValidationError("Email already registered with us")

class MessageForm(FlaskForm):
    recipient_no = StringField("Receiver's Phone Number", validators=[DataRequired(), Length(min=10, max=10)])
    message = TextAreaField('Content', validators=[DataRequired(), Length(max=150)])
    send = SubmitField('Send')

class ContactForm(FlaskForm):
    contact_name = StringField("Contact Name", validators=[DataRequired()])
    contact_no = StringField("Enter Mobile No", validators=[DataRequired(), Length(min=10, max=10)])
    gender = RadioField('Gender', choices=[('male','Male'),('female','Female')])
    add_contact = SubmitField("Add Contact")

    def validate_contact_no(self, contact_no):
        number = Contact.query.filter_by(contact_no=contact_no.data, owner_id=current_user.user_id).first()
        if number:
            raise ValidationError("Mobile number already added to contacts list")