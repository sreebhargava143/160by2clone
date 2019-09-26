from flask import url_for
from project.messages.message import send_message

def send_reset_link(user):
    token = user.get_reset_token()
    mobile_no = user.mobile_no
    password_reset_link = f'''To reset your password, visit the 
    following link:
    {url_for('users.reset_token', token=token, _external=True)}
    If you did not make this request then simply ignore this message and no changes will be made.
    '''
    response = send_message(mobile_no, password_reset_link)
    print (response.text)