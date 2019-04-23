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
import logging as l 



l.basicConfig(level=l.DEBUG)
l.debug('This will get logged')




        

class SetMeetingForm(FormAction):
   def name(self):
      return "meeting_manager"

   @staticmethod
   def required_slots(tracker):
      return [
         "name",
         "time"
      ]

   def validate(self, dispatcher, tracker, domain):
      slot_values = self.extract_other_slots(dispatcher, tracker, domain)
      slot = tracker.get_slot(REQUESTED_SLOT)
      
      if slot:
         slot_values.update(self.extract_requested_slot(dispatcher, tracker, domain))
         if slot_values:
            value= slot_values[slot]
            l.info("Slot is "+slot+" Value is "+value)
         if not slot_values:
            l.info("Value couldn't be extracted")
            if(slot=="name"):
               da= str((tracker.latest_message)['text'])
               slot_values['name'] = da
            if(slot=="time"):
               da= str((tracker.latest_message)['text'])
               slot_values['time'] = da
            

      return [SlotSet(slot, value) for slot, value in slot_values.items()]


   def submit(self, dispatcher, tracker, domain):
      dispatcher.utter_template("utter_thanks_for_pi", tracker)
      return []

################################################################################################
