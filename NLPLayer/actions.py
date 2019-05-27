import sys
sys.path.append("..")

from rasa_core_sdk import Action
from rasa_core_sdk.events import SlotSet
from rasa_core_sdk.events import Restarted
from rasa_core_sdk.forms import FormAction, REQUESTED_SLOT
from rasa_core_sdk.events import ConversationPaused, ConversationResumed, UserUtteranceReverted, UserUttered
from rasa_core_sdk.events import ActionExecuted, FollowupAction

import math
import json
from mylog import log
log.info("Inside Action Server")

from caller import Caller 
import duck  

call= Caller() 




        

class SetMeetingForm(FormAction):

   def name(self):
      return "meeting_manager"

   @staticmethod
   def required_slots(tracker):
      log.info("Get required slots")
      msg= str((tracker.latest_message)['text'])
      rs=['person']

      _, out= duck.get_duration(msg) 
      if(out==0):
         rs.append("duration")
      else:
         log.info("duration: {}".format(out))

      out= duck.get_time(msg)
      if(out=="{}"):
         rs.append("time")
      else:
         log.info("time: {}".format(out))
      return rs 

   def slot_mappings(self):
      log.info("Slot Mapping")
      return {
         "person": self.from_text(),
         "time": self.from_text(),
         "duration": self.from_text()
         }

   def validate(self, dispatcher, tracker, domain):
      log.info("Inside Validation")
      slot_values = self.extract_other_slots(dispatcher, tracker, domain)
      
      slot_to_fill = tracker.get_slot(REQUESTED_SLOT)
      log.info("Validation requested slot is {}".format(slot_to_fill))

      msg= str((tracker.latest_message)['text'])
      log.info("Latest msg is {}".format(msg))
      
      if slot_to_fill:
         slot_values.update(self.extract_requested_slot(dispatcher, tracker, domain))

      for slot, value in slot_values.items():
         if(slot == 'duration'):
            _, out= duck.get_duration(value) 
            if(out==0):
               slot_values['duration']= None 
            else:
               slot_values['duration']= out
         if(slot=='time'):
            out= duck.get_time(value)
            slot_values['time']= out    

      return [SlotSet(slot, value) for slot, value in slot_values.items()]
         
                

   def submit(self, dispatcher, tracker, domain):
      log.info("Submitting")
      log.info("Members: {}".format(tracker.get_slot("person")))
      log.info("Duration: {}".format(tracker.get_slot("duration")))
      log.info("Time: {}".format(tracker.get_slot("time")))
      
      #log.info(str(call.get_invites()))
      dispatcher.utter_template("utter_thanks_for_pi", tracker)
      return []

################################################################################################


class ActionDefaultFallback(Action):

   def name(self):
      return "action_default_fallback"

   def run(self, dispatcher, tracker, domain):
      dispatcher.utter_template('utter_default', tracker)
      return [UserUtteranceReverted()]



class ShowInviteAction(Action):

   def name(self):
      return "show_invites_action"

   def run(self, dispatcher, tracker, domain):
      dispatcher.utter_message("Showing Invites, please wait")
      invites= call.get_invites() 
      invites= json.loads(invites)      
      invites= invites['invites']
      for invite in invites:
         text= "Name: {}".format(invite['event_title'])
         text+= "\nBy:   {}".format(invite['invited_by'])
         buttons= [{
            'title': 'Accept',
            'payload': '/accept_invite{"invite_id":'+str(invite['id'])+'}'
         }]
         dispatcher.utter_button_message(
            text= text,
            buttons= buttons
         )
      return [] 



class AcceptInviteAction(Action):
   def name(self):
      return "accept_invite_action"

   def run(self, dispatcher, tracker, domain):
      dispatcher.utter_message("Accepting invite, please wait...")
      invite_id= tracker.get_slot("invite_id") 
      out= call.accept_invite(int(invite_id))
      dispatcher.utter_message(out) 


class ShowPendingEventStatus(Action):
   def name(self):
      return "show_pending_events_action"

   def run(self, dispatcher, tracker, domain):
      dispatcher.utter_message("Fatching details, please wait...")
      out= call.show_pending_event_status()
      out= json.loads(out)
      pending_events= out['pending_events']
      for pending_event in pending_events:
         text= pending_event['title']+"\n"
         text+="{} out of {} members accepted".format(pending_event['accepted'], pending_event['total'])
         buttons= [{
            'title': 'Show details',
            'payload': '/pending_event_details{"event_id":'+str(pending_event['id'])+'}'
         }]
         dispatcher.utter_button_message(
            text= text,
            buttons= buttons
         )
      return []


class PendingEventDetailAction(Action):
   def name(self):
      return "pending_event_detail_action"

   def run(self, dispatcher, tracker, domain):
      dispatcher.utter_message("Fatching event details, please wait...")
      event_id= tracker.get_slot("event_id") 
      out= call.pending_event_detail(int(event_id))
      dispatcher.utter_message(out) 
      