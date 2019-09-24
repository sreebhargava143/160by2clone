from project import app, db, encrypt
from flask import render_template, url_for, redirect, flash, get_flashed_messages, request
from flask_login import login_user, current_user, logout_user, login_required
from project.forms import LoginForm, SignUpForm
from project.models import User

@app.route('/', methods=["POST", "GET"])
@app.route('/index', methods=["POST", "GET"])
def login():
    form = LoginForm()
    if request.method == 'POST':
       flash(form.validate_on_submit())
        
    if form.validate_on_submit():
        user = User.query.filter_by(mobile_no=form.mobile_no.data).first()
        password_check = encrypt.check_password_hash(user.password, form.password.data)
        if user and password_check:
            login_user(user)
            return redirect(url_for('account'))
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
@app.route('/account')
def account():
    return f"LOGIN SUCCESS FULL FOR {current_user.username}"