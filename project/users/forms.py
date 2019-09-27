from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, RadioField
from project.models import User
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError


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

class RequestResetForm(FlaskForm):
    mobile_no = StringField('Mobile No',
                        validators=[DataRequired(), Length(min=10, max=10)])
    submit = SubmitField('Request Password Reset')

    def validate_mobile_no(self, mobile_no):
        user = User.query.filter_by(mobile_no=mobile_no.data).first()
        if user is None:
            raise ValidationError('There is no account with that email. You must SIGN-UP first.')


class ResetPasswordForm(FlaskForm):
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("Reset Password")