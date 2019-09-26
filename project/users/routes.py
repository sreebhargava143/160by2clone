from project import db, encrypt
from flask import render_template, url_for, redirect, flash, get_flashed_messages
from flask_login import login_user, current_user, logout_user, login_required
from project.users.forms import LoginForm, SignUpForm, RequestResetForm, ResetPasswordForm
from project.models import User
from project.users.utils import send_reset_link

from flask import Blueprint

users = Blueprint("users", __name__)

@users.route('/signup', methods=["POST", "GET"])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        password_hash = encrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email_id=form.email_id.data, mobile_no=form.mobile_no.data, password=password_hash)
        db.session.add(user)
        db.session.commit()
        flash("Registration Successfull", "done")
        return redirect(url_for('users.login', title="Login"))
    return render_template("signup.html", title="Sign Up", form=form)


@users.route('/', methods=["POST", "GET"])
@users.route('/index', methods=["POST", "GET"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('messages.message'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(mobile_no=form.mobile_no.data).first()
        if user:
            if encrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('messages.message'))
            else:
                flash("invalid password or username", "fail")
        else:
            flash("You are not a registered user! Register to login", "fail")
            return redirect(url_for('users.signup'))
    return render_template("login.html", form=form)



@users.route('/forgot_password', methods=["POST", "GET"])
def forgot_password():
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(mobile_no=form.mobile_no.data).first()
        send_reset_link(user)
        flash('A reset link has been sent with instructions to reset your registered mobile number.', 'done')
        return redirect(url_for('users.login'))
    return render_template('forgot_password.html', title='Reset Password', form=form)

@users.route("/forgot_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('users.forgot_password'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = encrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('users.login'))
    return render_template('reset_token.html', title='Reset Password', form=form)

@users.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('users.login'))

