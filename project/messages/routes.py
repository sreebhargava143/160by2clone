from project import db
from flask import render_template,url_for, redirect, flash, get_flashed_messages
from flask_login import current_user, login_required
from project.messages.forms import MessageForm
from project.models import Contact, Message
from sqlalchemy import and_
from project import moment
from project.messages.message import send_message
from flask import Blueprint

messages = Blueprint("messages", __name__)


@messages.route('/message', methods=["GET", "POST"])
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
        return redirect(url_for("messages.message", form=form, contacts=contacts))
    return render_template("message.html", form=form, contacts=contacts)

@messages.route('/message_to/<string:contact_no>', methods=["GET", "POST"])
@login_required
def message_to(contact_no):
    contacts = Contact.query.filter_by(owner_id=current_user.user_id).all()
    form = MessageForm()
    form.recipient_no.data = contact_no
    return render_template("message.html", form=form, contacts=contacts)

@messages.route('/sent_messages', methods=["GET", "POST"])
@login_required
def sent_messages():
    sent_messages = Message.query.filter_by(sender=current_user).order_by(Message.timestamp.desc())
    return render_template("sent.html", sent_messages=sent_messages)