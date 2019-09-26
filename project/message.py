import requests
import json
from project import app

URL = 'https://www.160by2.com/api/v1/sendCampaign'

# get request
def send_message(recipient_no, message):
  req_params = {
  'apikey':app.config["MESSAGE_API_KEY"],
  'secret':app.config["MESSAGE_SECRET_KEY"],
  'usetype':app.config["MESSAGE_USE_TYPE"],
  'phone': recipient_no,
  'message':message,
  'senderid':app.config["SENDER_ID"]
  }
  req_url = app.config["MESSAGE_URL"]
  print(req_params, req_url)
  return requests.post(req_url, req_params)

# get response
# response = sendPostRequest(URL, 'provided-api-key', 'provided-secret', 'prod/stage', 'valid-to-mobile', 'active-sender-id', 'message-text' )
# """
#   Note:-
#     you must provide apikey, secretkey, usetype, mobile, senderid and message values
#     and then requst to api
# """
# print response if you want
# print (response.text)