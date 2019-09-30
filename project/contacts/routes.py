from project import db
from flask import render_template, url_for, redirect, flash, get_flashed_messages
from flask_login import current_user, login_required
from project.contacts.forms import ContactForm
from project.models import Contact
from sqlalchemy import and_

from flask import Blueprint

contacts = Blueprint("contacts", __name__)


@contacts.route('/contact', methods=["GET", "POST"])
@login_required
def contact():
    contacts = Contact.query.filter_by(owner_id=current_user.id).all()
    form = ContactForm()
    if form.validate_on_submit():
        contact = Contact(contact_name=form.contact_name.data, contact_no=form.contact_no.data, owner=current_user, gender=form.gender.data)
        db.session.add(contact)
        db.session.commit()
        flash("contact added", "success")
        return redirect(url_for('contacts.contact'))
    return render_template("contact.html", form=form, contacts=contacts, title='contact')

@contacts.route('/delete_contact', methods=["GET", "POST"])
@login_required
def delete_contact():
    contacts = Contact.query.filter_by(owner_id=current_user.id).all()
    form = ContactForm()
    if form.validate_on_submit():
        print("Entered delete")
        contact = Contact.query.filter(and_(Contact.contact_no==form.contact_no.data, Contact.owner==current_user)).first()
        print(contact)
        db.session.delete(contact)
        db.session.commit()
        flash("contact deleted", "danger")
    return render_template("contact.html", form=form, contacts=contacts)

@contacts.route('/delete_selected/<string:contact_no>', methods=["GET", "POST"])
@login_required
def delete_selected(contact_no):
    contacts = Contact.query.filter_by(owner_id=current_user.id).all()
    contact = Contact.query.filter(and_(Contact.owner==current_user, Contact.contact_no==contact_no)).first()
    form = ContactForm()
    form.contact_no.data = contact_no
    form.contact_name.data = contact.contact_name
    form.gender.data = contact.gender
    return render_template("contact.html", title="delete_contact", form=form, contacts=contacts)