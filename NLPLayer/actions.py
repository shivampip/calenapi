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

   adata={}

   @staticmethod
   def required_slots(tracker):
      log.info("Get required slots")
      msg= str((tracker.latest_message)['text'])
      rs=['person', 'title']

      if('duration' not in SetMeetingForm.adata):
         _, out= duck.get_duration(msg) 
         if(out==0):
            rs.append("duration")
         else:
            SetMeetingForm.adata['duration']= out 
            log.info("duration: {}".format(out))

      if('time' not in SetMeetingForm.adata):
         out= duck.get_time(msg)
         if(out=="{}"):
            rs.append("time")
         else:
            SetMeetingForm.adata['time']= out 
            log.info("time: {}".format(out))
      
      log.info("Required Slots are: {}".format(str(rs)))
      return rs 

   def slot_mappings(self):
      log.info("Slot Mapping")
      return {
         "person": self.from_text(),
         "time": self.from_text(),
         "duration": self.from_text(),
         "title": self.from_text()
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
            if(len(out)>0):
               slot_values['time']= out    
            else:
               slot_values[   'time']= None 
      return [SlotSet(slot, value) for slot, value in slot_values.items()]
         
                

   def submit(self, dispatcher, tracker, domain):
      log.info("Submitting")
      md= {}
      md['title']= tracker.get_slot("title")
      md['members']= tracker.get_slot("person")

      if('duration' in SetMeetingForm.adata):
         md['duration']= SetMeetingForm.adata['duration']
      else:
         md['duration']= tracker.get_slot("duration")
      md['duration']= int(md['duration'])

      if('time' in SetMeetingForm.adata):
         ttime= SetMeetingForm.adata['time']
      else:
         ttime= tracker.get_slot("time")
      md['from_dt']= ttime['from']
      if('to' in ttime):
         md['to_dt']= ttime['to']
      else:
         tto= duck.add_duration(duck.str_to_dt(md['from_dt']), md['duration'])
         md['to_dt']= tto.strftime("%Y-%m-%dT%H:%M")
         
      log.info(str(md))

      out= call.get_best_available_slots(md['from_dt'], md['to_dt'], md['duration'])
      out= json.loads(out)
      if(out['status']=='success'):
         #dispatcher.utter_message("Response:- {}".format(out))
         data= out['data']
         md['from']= dt_from= data['from']
         md['to']= dt_to= data['to']
         dt_from= duck.str_to_dt(dt_from)
         dt_to= duck.str_to_dt(dt_to)
         text= "On {}, are you fine with {} to {}".format(duck.dt_to_date(dt_from), duck.dt_to_time(dt_from), duck.dt_to_time(dt_to))
         buttons= []
         buttons.append({"title":"Book", 'payload': '/book_meeting', 'type': "postback"})
         buttons.append({"title":"Show more slots", 'payload': '/show_more_slots', 'type': "postback"})

         dispatcher.utter_button_message(
            text= text,
            buttons= buttons
         )

      else:
         dispatcher.utter_message("Response me Error aa gyi")

      return [SlotSet("meeting_data", json.dumps(md) )]

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
      