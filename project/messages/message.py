import requests
import json
from flask import current_app

URL = 'https://www.160by2.com/api/v1/sendCampaign'

# get request
def send_message(recipient_no, message):
  req_params = {
  'apikey':current_app.config["MESSAGE_API_KEY"],
  'secret':current_app.config["MESSAGE_SECRET_KEY"],
  'usetype':current_app.config["MESSAGE_USE_TYPE"],
  'phone': recipient_no,
  'message':message,
  'senderid':current_app.config["SENDER_ID"]
  }
  req_url = current_app.config["MESSAGE_URL"]
  print(req_params, req_url)
  return requests.post(req_url, req_params)