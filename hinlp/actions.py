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

from calen import forchat
l.debug("FORCHAT imported")



l.basicConfig(level=l.DEBUG)
l.debug('This will get logged')




        

class SetMeetingForm(FormAction):

   def name(self):
      return "meeting_manager"

   @staticmethod
   def required_slots(tracker):
      print("##### In Meeting Form Action")
      return [
         "person",
         "time",
         "duration"
      ]

   def slot_mappings(self):
      print("inside slot_mappings")
      return {
         "person": self.from_text(),
         "time": self.from_text(),
         "duration": self.from_text()
         }


   def validate(self, dispatcher, tracker, domain):
      print("inside validate")
      slot_values = self.extract_other_slots(dispatcher, tracker, domain)
      slot_to_fill = tracker.get_slot(REQUESTED_SLOT)
      if slot_to_fill:
            slot_values.update(self.extract_requested_slot(dispatcher, tracker, domain))
      
      for slot, value in slot_values.items():
         print("### Slot: {}, Value: {}".format(slot, value))
         
      return [SlotSet(slot, value) for slot, value in slot_values.items()]

   def submit(self, dispatcher, tracker, domain):
      dispatcher.utter_template("utter_thanks_for_pi", tracker)
      return []

################################################################################################


class ActionDefaultFallback(Action):

   def name(self):
      return "action_default_fallback"

   def run(self, dispatcher, tracker, domain):
      dispatcher.utter_template('utter_default', tracker)
      return [UserUtteranceReverted()]
