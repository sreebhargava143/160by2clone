from datetime import datetime
from project import app, db, login_manager
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from project.search import add_to_index, remove_from_index, query_index


class SearchableMixin(object):
    @classmethod
    def search(cls, expression, page, per_page):
        ids, total = query_index(cls.__tablename__, expression, page, per_page)
        if total == 0:
            return cls.query.filter_by(id=0), 0
        when = []
        for i in range(len(ids)):
            when.append((ids[i], i))
        return cls.query.filter(cls.id.in_(ids)).order_by(
            db.case(when, value=cls.id)), total

    @classmethod
    def before_commit(cls, session):
        session._changes = {
            'add': list(session.new),
            'update': list(session.dirty),
            'delete': list(session.deleted)
        }

    @classmethod
    def after_commit(cls, session):
        for obj in session._changes['add']:
            if isinstance(obj, SearchableMixin):
                add_to_index(obj.__tablename__, obj)
        for obj in session._changes['update']:
            if isinstance(obj, SearchableMixin):
                add_to_index(obj.__tablename__, obj)
        for obj in session._changes['delete']:
            if isinstance(obj, SearchableMixin):
                remove_from_index(obj.__tablename__, obj)
        session._changes = None

    @classmethod
    def reindex(cls):
        for obj in cls.query:
            add_to_index(cls.__tablename__, obj)

db.event.listen(db.session, 'before_commit', SearchableMixin.before_commit)
db.event.listen(db.session, 'after_commit', SearchableMixin.after_commit)


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), nullable=False)
    mobile_no = db.Column(db.String(10), index=True, unique=True, nullable=False)
    gender = db.Column(db.String(10))
    email_id = db.Column(db.String(30),nullable=False, index=True, unique=True)
    password = db.Column(db.String(60), nullable=False)
    contacts = db.relationship('Contact', backref='owner', lazy='dynamic')
    messages_sent = db.relationship('Message', backref="sender", lazy="dynamic")

    def get_id(self):
        return int(self.id)

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            id = s.loads(token)['id']
        except:
            return None
        return User.query.get(id)

    def __repr__(self):
        return f"Username: {self.username} Mobile No: {self.mobile_no}"

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    contact_name = db.Column(db.String(30), index=True, nullable=False)
    contact_no = db.Column(db.String(10), index=True, nullable=False)
    gender = db.Column(db.String(10))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    messages_received = db.relationship("Message", backref="recipient", lazy="dynamic")

    def __repr__(self):
        return f"Contact Name: {self.contact_name} Mobile No: {self.contact_no}"

class Message(SearchableMixin, db.Model):
    __searchable__ = ['message_body']
    id = db.Column(db.Integer, primary_key=True, index=True)
    message_body = db.Column(db.String(150), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.now)
    sender_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    recipient_id = db.Column(db.Integer, db.ForeignKey("contact.id"))

    def __repr__(self):
        return f"Message: {self.message_body} sender: {self.sender.username} recipient: {self.recipient.contact_name}"