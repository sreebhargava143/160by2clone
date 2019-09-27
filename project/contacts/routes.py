from project import db
from flask import render_template, url_for, redirect, flash, get_flashed_messages
from flask_login import current_user, login_required
from project.contacts.forms import ContactForm
from project.models import Contact

from flask import Blueprint

contacts = Blueprint("contacts", __name__)


@contacts.route('/contact', methods=["GET", "POST"])
@login_required
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        contact = Contact(contact_name=form.contact_name.data, contact_no=form.contact_no.data, owner=current_user)
        db.session.add(contact)
        db.session.commit()
        flash("contact added", "success")
        return redirect(url_for('contacts.contact'))
    return render_template("contact.html", form=form)

