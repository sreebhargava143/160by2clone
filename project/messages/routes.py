from project import db
from flask import render_template,url_for, redirect, flash, get_flashed_messages, request, current_app
from flask_login import current_user, login_required
from project.messages.forms import MessageForm, SearchForm
from project.models import Contact, Message
from sqlalchemy import and_
from project import moment
from project.messages.message import send_message
from flask import Blueprint
from flask import g

messages = Blueprint("messages", __name__)


@messages.route('/message', methods=["GET", "POST"])
@login_required
def message():
    contacts = Contact.query.filter_by(owner_id=current_user.id).all()
    form = MessageForm()
    if form.validate_on_submit():
        # response = send_message(form.recipient_no.data, form.message.data)
        # print(response.text)
        # print(type(response.text))
        # print(response.status_code, type(response.status_code))
        # print(response.json())
        # if response.status_code == 200:
        recipient = Contact.query.filter(and_(Contact.contact_no==form.recipient_no.data, Contact.owner==current_user)).first()
        message = Message(message_body=form.message.data, sender=current_user, recipient=recipient)
        db.session.add(message)
        db.session.commit()
        flash("message sent", "success")
        return redirect(url_for("messages.message", form=form, contacts=contacts))
    return render_template("message.html", form=form, contacts=contacts)

@messages.route('/message_to/<string:contact_no>', methods=["GET", "POST"])
@login_required
def message_to(contact_no):
    contacts = Contact.query.filter_by(owner_id=current_user.id).all()
    form = MessageForm()
    form.recipient_no.data = contact_no
    return render_template("message.html", form=form, contacts=contacts)

@messages.route('/sent_messages', methods=["GET", "POST"])
@login_required
def sent_messages():
    contacts = Contact.query.filter_by(owner_id=current_user.id).all()

    page = request.args.get('page', 1, type=int)

    sent_messages_list = Message.query.filter_by(sender=current_user).order_by(Message.timestamp.desc()).paginate(page=page, per_page=current_app.config['MESSAGES_PER_PAGE'])
    
    next_url = url_for("messages.sent_messages", page=sent_messages_list.next_num) if sent_messages_list.has_next else None
    
    prev_url = url_for("messages.sent_messages", page=sent_messages_list.prev_num) if sent_messages_list.has_prev else None
    
    return render_template("sent.html", sent_messages=sent_messages_list.items, contacts=contacts, next_url=next_url, prev_url=prev_url)

@messages.route('/sent_messages_of/<string:recipient_no>', methods=["GET", "POST"])
@login_required
def sent_messages_of(recipient_no):
    contacts = Contact.query.filter_by(owner_id=current_user.id).all()
    page = request.args.get('page', 1, type=int)

    
    recipient = Contact.query.filter_by(contact_no=recipient_no).first()
    sent_messages_list = Message.query.filter(and_(Message.sender==current_user, Message.recipient==recipient)).order_by(Message.timestamp.desc()).paginate(page=page, per_page=current_app.config['MESSAGES_PER_PAGE'])

    next_url = url_for("messages.sent_messages", page=sent_messages_list.next_num) if sent_messages_list.has_next else None

    prev_url = url_for("messages.sent_messages", page=sent_messages_list.prev_num) if sent_messages_list.has_prev else None

    return render_template("sent.html", sent_messages=sent_messages_list.items, contacts=contacts, next_url=next_url, prev_url=prev_url)

@messages.before_app_request
def before_request():
    if current_user.is_authenticated:
        g.search_form = SearchForm()

@messages.route('/search')
@login_required
def search():
    contacts = Contact.query.filter_by(owner_id=current_user.id).all()
    if not g.search_form.validate():
        return redirect(url_for('message.sent_messages'))
    page = request.args.get('page', 1, type=int)
    messages, total = Message.search(g.search_form.q.data, page,
                               current_app.config['MESSAGES_PER_PAGE'])
    next_url = url_for('messages.search', q=g.search_form.q.data, page=page + 1) if total > page * current_app.config['MESSAGES_PER_PAGE'] else None
    prev_url = url_for('messages.search', q=g.search_form.q.data, page=page - 1) if page > 1 else None
    return render_template('sent.html', title='Search', sent_messages=messages,contacts=contacts, next_url=next_url, prev_url=prev_url)
