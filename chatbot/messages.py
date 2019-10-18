#These are the messages that are send to the user at various stages

intro_message = "Hi, I'm an interface for providing sounds for the museum of sound project. Please record a sound."
prompt_for_description = "Thanks for sending me a sound, please provide a description or upload a new sound."
confirmation = "Your sound has been uploaded. Thanks for contributing to the project!"
rate_limit = "Please wait 3 minutes before sending another sound."
error = "Sorry, there's been an error. Please try again later"
wrong_attachment = "Sorry, I can't accept other attachments. Please record a sound."

#Library imports
import requests, json, os, sys
from time import sleep

#Global var imports TODO Set these in setup.py
from os.path import join, dirname
from dotenv import load_dotenv
dotenv_path = join('../adminportal/', '.env')
load_dotenv(dotenv_path)

#JSON Template for creating the confirmation a sound has been uploaded to the database
def create_confirmation(sender_id, sound_desc, sound_url):
    response = {
        "recipient":{
        "id": sender_id
     },
     "message":{
      "attachment": {
        "type": "template", "payload":
            {"template_type": "generic","elements": [{
            "title": "Here's your sound:",
            "subtitle":sound_desc,
            "default_action": {
                "type": "web_url",
                "url": sound_url,
                "webview_height_ratio": "compact"
            },
          }]
        }
        }
    }
    }
    return json.dumps(response)

#Single interface for sending requests to the FB messages API
def send_message_request(params, headers, data):
    try:
        r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
        print ("sent message: ", r, r.json())
        return r
    except requests.exceptions.Timeout as errt:
        print ("Timeout Error:",errt, file =sys.stderr)
        time.sleep(0.5)
        try:
            requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
        except:
            print ("Secondary Timeout Error:",errt, file =sys.stderr)
    except requests.exceptions.RequestException as err:
        print ("Send Message Error: ",err , file =sys.stderr)

#JSON Template for sending simple text message
def send_message(recipient_id, message_text):
    params = {
        "access_token": os.environ["PAGE_ACCESS_TOKEN"]
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "text": message_text
        }
    })
    return send_message_request(params, headers, data)

#Second part of JSON template for confirmation
def send_confirmation(sender_id, sound_desc, sound_url):
    params = {
        "access_token": os.environ["PAGE_ACCESS_TOKEN"]
    }
    headers = {
        "Content-Type": "application/json"
    }
    response = create_confirmation(sender_id, sound_desc, sound_url)
    return send_message_request(params, headers, response)
