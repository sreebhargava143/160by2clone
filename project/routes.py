from project import app, db, encrypt
from flask import render_template, url_for, redirect, flash, get_flashed_messages, request
from flask_login import login_user, current_user, logout_user, login_required
from project.forms import LoginForm, SignUpForm, MessageForm, ContactForm, RequestResetForm, ResetPasswordForm
from project.models import User, Contact, Message
from sqlalchemy import and_
from project import moment
from project.message import send_message

@app.route('/', methods=["POST", "GET"])
@app.route('/index', methods=["POST", "GET"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('message'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(mobile_no=form.mobile_no.data).first()
        if user:
            if encrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('message'))
            else:
                flash("invalid password or username", "fail")
        else:
            flash("You are not a registered user! Register to login", "fail")
            return redirect(url_for('signup'))
    return render_template("login.html", form=form)

@app.route('/signup', methods=["POST", "GET"])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        password_hash = encrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email_id=form.email_id.data, mobile_no=form.mobile_no.data, password=password_hash)
        db.session.add(user)
        db.session.commit()
        flash("Registration Successfull", "done")
        return redirect(url_for('login', title="Login"))
    return render_template("signup.html", title="Sign Up", form=form)

@app.route('/message', methods=["GET", "POST"])
@login_required
def message():
    contacts = Contact.query.filter_by(owner_id=current_user.user_id).all()
    form = MessageForm()
    if form.validate_on_submit():
        response = send_message(form.recipient_no.data, form.message.data)
        print(response.text)
        print(type(response.text))
        print(response.status_code, type(response.status_code))
        print(response.json())
        if response.status_code == 200:
            recipient = Contact.query.filter(and_(Contact.contact_no==form.recipient_no.data, Contact.owner==current_user)).first()
            message = Message(message_body=form.message.data, sender=current_user, recipient=recipient)
            db.session.add(message)
            db.session.commit()
            flash("message sent", "done")
        return redirect(url_for("message", form=form, contacts=contacts))
    return render_template("message.html", form=form, contacts=contacts)

@app.route('/message_to/<string:contact_no>', methods=["GET", "POST"])
@login_required
def message_to(contact_no):
    contacts = Contact.query.filter_by(owner_id=current_user.user_id).all()
    form = MessageForm()
    form.recipient_no.data = contact_no
    return render_template("message.html", form=form, contacts=contacts)

@app.route('/sent_messages', methods=["GET", "POST"])
@login_required
def sent_messages():
    sent_messages = Message.query.filter_by(sender=current_user).order_by(Message.timestamp.desc())
    return render_template("sent.html", sent_messages=sent_messages)

@app.route('/contact', methods=["GET", "POST"])
@login_required
def contact():
    form = ContactForm()
    if request.method == "GET":
        form.contact_name.data = ""
        form.contact_no.data = ""
    if form.validate_on_submit():
        contact = Contact(contact_name=form.contact_name.data, contact_no=form.contact_no.data, owner=current_user)
        db.session.add(contact)
        db.session.commit()
        flash("contact added", "done")
        return redirect(url_for('contact'))
    return render_template("contact.html", form=form)

def send_reset_email(user):
    token = user.get_reset_token()
    mobile_no = user.mobile_no
    password_reset_link = f'''To reset your password, visit the 
    following link:
    {url_for('reset_token', token=token, _external=True)}
    If you did not make this request then simply ignore this email and no changes will be made.
    '''
    response = send_message(mobile_no, password_reset_link)
    print (response.text)

@app.route('/forgot_password', methods=["POST", "GET"])
def forgot_password():
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(mobile_no=form.mobile_no.data).first()
        send_reset_email(user)
        flash('A reset link has been sent with instructions to reset your registered mobile number.', 'done')
        return redirect(url_for('login'))
    return render_template('forgot_password.html', title='Reset Password', form=form)

@app.route("/forgot_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('forgot_password'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = encrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('reset_token.html', title='Reset Password', form=form)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))
