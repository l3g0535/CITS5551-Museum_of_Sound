from django.views import generic
from django.http.response import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
#User State Descriptions
#0 : user has not provided a recording and has not been sent prompt
#1 : user has been send prompt but not provided recording
#2 : user has provided recording but no description
#3 : user has provided sound and is rate limited

import json

from dotenv import load_dotenv
from os.path import join
from . import messages
from .db_functs import *
from datetime import timedelta
from django.utils import timezone
from .models import PendingSound
#Needed to import API authentication codes
# dotenv_path = join('../adminportal/', '.env')
# load_dotenv(dotenv_path)

USER_RATE_LIMIT = 1
CHAT_LENGTH = 3

# Create your views here.

class fbBotView(generic.View):

    #Verifies the Facebook messenger API
    def get(self, request, *args, **kwargs):
        if self.request.GET['hub.verify_token'] == 'abc123':
            return HttpResponse(self.request.GET['hub.challenge'])
        else:
            return HttpResponse('Error, invalid token')

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        if request.method == 'GET':
            return self.get(self, request, *args, **kwargs)
        elif request.method == 'POST':
            return self.post(self, request, *args, **kwargs)

    #All new messages are accepted through this function
    def post(self, request, *args, **kwargs):
        # endpoint for processing incoming messaging events
        data = json.loads(self.request.body.decode('utf-8'))
        #log(data)  # you may not want to log every incoming message in production, but it's good for testing
        if data["object"] == "page":
            for entry in data["entry"]:
                process_message(entry)
        return HttpResponse('/success/')

#Processes message according to user state and type of message (text of attachment)
def process_message(entry):
    for messaging_event in entry["messaging"]:
        sender_id = messaging_event["sender"]["id"] # the facebook ID of the person sending you the message
        if messaging_event.get("message"):  # someone sent us a message)
            print(messaging_event.get("message"))
            user_state = check_userstate(sender_id)

            #State 0: User hasn't received prompt and haven't sent a recording yet
            if (user_state == 0):
                handle_state_0(sender_id, messaging_event)

            #State 1: User has been sent prompt, only accepts recordings
            elif (user_state == 1):
                handle_state_1(sender_id, messaging_event)

            #State 2: User has sent a sound and has received desc. prompt
            elif user_state == 2:
                handle_state_2(sender_id, messaging_event)

            #State 3: User has provided sound and description, now rate_limited
            elif user_state == 3:
                handle_state_3(sender_id)

def handle_state_0(sender_id, messaging_event):
    if "text" in messaging_event["message"]:
        messages.send_message(sender_id, messages.intro_message)
        update_userstate(sender_id,1)
    elif "attachments" in messaging_event["message"]:
        handle_attachments(messaging_event, sender_id)

def handle_state_1(sender_id, messaging_event):
    if "attachments" in messaging_event["message"]:
        handle_attachments(messaging_event, sender_id)

def handle_state_2(sender_id, messaging_event):
    if "text" in messaging_event["message"]:
        description = messaging_event["message"]["text"]
        print("HERE _________________\n")
        print(sender_id)
        print(PendingSound.objects.all())
        sound_url = PendingSound.objects.filter(user__user_id=sender_id).first().remote_location
        upload_to_db(sender_id, sound_url, description)
        PendingSound.objects.filter(user_id=sender_id).delete()
        messages.send_message(sender_id, messages.confirmation)
        update_userstate(sender_id, 3)
    elif "attachments" in messaging_event["message"]:
        handle_attachments(messaging_event, sender_id)

def handle_state_3(sender_id):
    messages.send_message(sender_id, messages.rate_limit)

def check_userstate(sender_id):
    user_info = FBUser.objects.filter(user_id=sender_id).first()
    if user_info is None:
        user = FBUser(user_id=sender_id,state=0)
        user.save()
        return 0
    elif user_info.time_of_last < timezone.now() - timedelta(minutes=CHAT_LENGTH):
        update_userstate(sender_id,0)
        PendingSound.objects.filter(user__user_id=sender_id).delete()
        return 0
    elif user_info.state == 3:
        if user_info.time_of_last < timezone.now() - timedelta(minutes=USER_RATE_LIMIT):
            update_userstate(sender_id,0)
            return 0
        else:
            return 3
    else:
        return user_info.state

#Handles sounds being uploded deals with users in state 1
def handle_attachments(messaging_event, sender_id):
    if messaging_event["message"]["attachments"][0]["type"] == "audio":
        recording = messaging_event["message"]["attachments"][0]["payload"]["url"]
        pending_sound = PendingSound(user_id = sender_id, remote_location = recording)
        pending_sound.save()
        messages.send_message(sender_id, messages.prompt_for_description)
        update_userstate(sender_id,2)
    else:
        messages.send_message(sender_id, messages.wrong_attachment)
        update_userstate(sender_id,1)
