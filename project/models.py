from datetime import datetime
from project import app, db, login_manager
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), nullable=False)
    mobile_no = db.Column(db.String(10), index=True, unique=True, nullable=False)
    gender = db.Column(db.String(10))
    email_id = db.Column(db.String(30),nullable=False, index=True, unique=True)
    password = db.Column(db.String(60), nullable=False)
    contacts = db.relationship('Contact', backref='owner', lazy='dynamic')
    messages_sent = db.relationship('Message', backref="sender", lazy="dynamic")

    def get_id(self):
        return int(self.user_id)

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.user_id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"Username: {self.username} Mobile No: {self.mobile_no}"

class Contact(db.Model):
    contact_id = db.Column(db.Integer, primary_key=True)
    contact_name = db.Column(db.String(30), index=True, nullable=False)
    contact_no = db.Column(db.String(10), index=True, nullable=False)
    gender = db.Column(db.String(10))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    messages_received = db.relationship("Message", backref="recipient", lazy="dynamic")

    def __repr__(self):
        return f"Contact Name: {self.contact_name} Mobile No: {self.contact_no}"

class Message(db.Model):
    message_id = db.Column(db.Integer, primary_key=True)
    message_body = db.Column(db.String(150), nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.now)
    sender_id = db.Column(db.Integer, db.ForeignKey("user.user_id"))
    recipient_id = db.Column(db.Integer, db.ForeignKey("contact.contact_id"))

    def __repr__(self):
        return f"Message: {self.message_body} sender: {self.sender.username} recipient: {self.recipient_id}"