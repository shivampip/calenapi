import sys
sys.path.append("..")

from rasa_core_sdk import Action
from rasa_core_sdk.events import SlotSet
from rasa_core_sdk.events import Restarted, AllSlotsReset
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

'''
class Restarted(Action):

   def name(self):
      return 'action_restarted'
      

   def run(self, dispatcher, tracker, domain):
      dispatcher.utter_message("Resetarting...")
      return [Restarted(), AllSlotsReset()]
   '''   

        

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
            log.info("VALIDATING DURATION: {}".format(out))
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

      try:
         md['duration']= int(md['duration'])
      except ValueError:
         _, out= duck.get_duration(md['duration']) 
         md['duration']= int(out)
         if(md['duration']==0):
            dispatcher.utter_message("Error while booking")
            return []

      if('time' in SetMeetingForm.adata):
         ttime= SetMeetingForm.adata['time']
      else:
         ttime= tracker.get_slot("time")
      
      if('from' not in ttime):
         ttime= duck.get_time(ttime)
         if(ttime=="{}"):
            dispatcher.utter_message("Error while booking")
            return []

      md['from_dt']= ttime['from']
      if('to' in ttime):
         md['to_dt']= ttime['to']
      else:
         log.info("combining duration for dt_end")
         tto= duck.add_duration(duck.str_to_dt(md['from_dt']), md['duration'])
         md['to_dt']= tto.strftime("%Y-%m-%dT%H:%M")
         
      log.info(str(md))
      SetMeetingForm.adata= {}

      out= call.get_best_available_slots(md['from_dt'], md['to_dt'], md['duration'])
      out= json.loads(out)
      log.info("\nOUT: {}".format(str(out)))
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

         return [SlotSet("meeting_data", json.dumps(md) )]

      elif(out['status']=='error'):
         dispatcher.utter_message(out['data'])
         return []
      else:
         dispatcher.utter_message("Unknown error occured")
         return []

      



class ActionBookMeeting(Action):
    
   def name(self):
      return "action_book_meeting"


   def run(self, dispatcher, tracker, domain):
      dispatcher.utter_message("Booking, please wait..")

      md= tracker.get_slot("meeting_data")
      md= json.loads(md)
      #dispatcher.utter_message("Data is {}".format(md))
      
      title= md['title']
      dt_from= duck.make_std(md['from'])
      dt_to= duck.make_std(md['to'])
      include_author= True 
      members= md['members']

      out= call.make_pending_event(title, dt_from, dt_to, include_author, members) 
      #dispatcher.utter_message("RESPONSE: {}".format(str(out)))
      out= json.loads(out)
      status= out['status']
      if(status=='success'):
         dispatcher.utter_message("Meeting booked successfully")
         data= out['data']
         pout= "**"+data['title']+"**\n"
         dt= duck.str_to_dt(data['date_start'])
         ddt= dt.date()
         pout+= "Date: {}\n".format(ddt)
         ts= dt.strftime("%H:%M")
         te= duck.str_to_dt(data['date_end']).strftime("%H:%M")
         pout+= "Time: {} - {}\n".format(ts, te)
         pout+= "Members: _"
         for member in json.loads(data['members']):
            pout+= member+", "
         pout+="_"
         #pout+= "\n **Bold** and *italic* and _pata_"
         dispatcher.utter_message(pout)
      elif(status=='error'):
         dispatcher.utter_message("Error: {}".format(out['data']))
      else:
         dispatcher.utter_message("Unknown error occured")

      return []


class ActionShowMoreSlots(Action):

   def name(self):
      return "action_show_more_slots"


   def run(self, dispatcher, tracker, domain):
      dispatcher.utter_message("Searching more slots....")

      md= tracker.get_slot("meeting_data")
      md= json.loads(md)
      log.info("Data is {}".format(md))
      
      dt_from= md['from_dt']
      dt_to= md['to_dt']
      duration= md['duration']

      out= call.get_available_slots(dt_from, dt_to, duration)
      out= json.loads(out)
      log.info("\AVAILABLE SLOTS: {}".format(str(out)))
      if(out['status']=='success'):
         #dispatcher.utter_message("Response:- {}".format(out))
         data= out['data']
         if(len(data)==1):
            dispatcher.utter_message("No other slot available in given timeframe")
            return []
         if(len(data)>5):
            dispatcher.utter_message("Due to platform limits, showing only first 5 slots")
            data= data[:5]
         for dd in data:
            dt_from= dd['from']
            dt_to= dd['to']
            dt_from= duck.str_to_dt(dt_from)
            dt_to= duck.str_to_dt(dt_to)
            timef= {"from": dd['from'], "to": dd['to']}
            timef= json.dumps(timef)
            text= "On {}, From {} to {}".format(duck.dt_to_date(dt_from), duck.dt_to_time(dt_from), duck.dt_to_time(dt_to))
            buttons= []
            buttons.append({"title":"Select Timeslot", 'payload': '/select_slot{"timeframe":'+timef+'}' })
            dispatcher.utter_button_message(
               text= text,
               buttons= buttons
            )



      return []


class ActionSelectSlot(Action):

   def name(self):
      return "action_select_slot"


   def run(self, dispatcher, tracker, domain):
      #dispatcher.utter_message("In Selected Timeframe")

      timef= tracker.get_slot("timeframe")
      log.info("TIMEFRAME: {}".format(timef))
      #dispatcher.utter_message("TIMEFRAME: {}".format(timef))
      
      #dispatcher.utter_message("Type: {}".format(type(timef)))
      #timef= json.loads(timef) 

      md= tracker.get_slot("meeting_data")
      md= json.loads(md) 

      md['from']= dt_from= timef['from']
      md['to']= dt_to= timef['to']
      dt_from= duck.str_to_dt(dt_from)
      dt_to= duck.str_to_dt(dt_to)
      text= "On {}, are you fine with {} to {}".format(duck.dt_to_date(dt_from), duck.dt_to_time(dt_from), duck.dt_to_time(dt_to))
      buttons= []
      buttons.append({"title":"Book", 'payload': '/book_meeting', 'type': "postback"})
      dispatcher.utter_button_message(
         text= text,
         buttons= buttons
      )
      return [SlotSet("meeting_data", json.dumps(md) )]

################################################################################################


class ActionDefaultFallback(Action):

   def name(self):
      return "action_default_fallback"

   def run(self, dispatcher, tracker, domain):
      #sender_id= tracker.sender_id 
      #dispatcher.utter_message("Sender ID is {}".format(sender_id))
      dispatcher.utter_template("utter_default", tracker)
      return [UserUtteranceReverted()]



from time import sleep

class ShowInviteAction(Action):

   def name(self):
      return "show_invites_action"

   def run(self, dispatcher, tracker, domain):
      log.info("Inside Showing inviets")
      #dispatcher.utter_message("Showing Invites, please wait")
      invites= call.get_invites()
      log.info("Got invites") 
      invites= json.loads(invites)      
      invites= invites['invites']
      log.info("Invites are: {}".format(str(invites)))
      if(len(invites)==0):
         dispatcher.utter_message("You have no invite pending")
         return []
      for invite in invites:
         log.info("Next Invite is: {}".format(invite))
         text= "Name: {}".format(invite['event_title'])
         text+= "\nBy:   {}".format(invite['invited_by'])
         buttons= [{
            'title': 'Accept',
            'payload': '/accept_invite{"invite_id":'+str(invite['id'])+'}'
         },{
            'title': 'Decline',
            'payload': '/accept_invite{"invite_id":'+str(invite['id'])+'}'
         }]
         dispatcher.utter_button_message(
            text= text,
            buttons= buttons
         )
      
      return [] 


class ActionNoti(Action):
   def name(self):
      return "action_noti"

   def run(self, dispatcher, tracker, domain):
      #dispatcher.utter_message("Fatching notifications, please wait...")
      out= call.get_notifications()
      out= json.loads(out) 
      if(out['status']=='success'):
         data= out['data']
         if(len(data)==0):
            dispatcher.utter_message("No notification")
            return []
         for noti in data:
            text= noti['text']
            data= noti['data']
            if(data==""):
               dispatcher.utter_message(text)
            else:
               data= json.loads(data)
               #log.info("PAYLOAD: {}".format("/"+data['intent']+"{'id':"+str(data['id'])+"}"))
               buttons= [{
                  'title': data['text'],
                  'payload': "/"+data['intent']+'{"'+data['param']+'":'+str(data['value'])+"}"
               }]
               dispatcher.utter_button_message(
                  text= text,
                  buttons= buttons
               )
               log.info("Button was {}".format(str(buttons)))
      else:
         dispatcher.utter_message("Couldn't fatch notifications") 

   

class AcceptInviteAction(Action):
   def name(self):
      return "accept_invite_action"

   def run(self, dispatcher, tracker, domain):
      #dispatcher.utter_message("Accepting invite, please wait...")
      invite_id= tracker.get_slot("invite_id") 
      out= call.accept_invite(int(invite_id))
      out= json.loads(out)
      if(out['status']=='success'):
         dispatcher.utter_message("Invite accepted successfully")
      else:
         dispatcher.utter_message("Error while accepting invite.") 


class ShowPendingEventStatus(Action):
   def name(self):
      return "show_pending_events_action"

   def run(self, dispatcher, tracker, domain):
      dispatcher.utter_message("Fatching details, please wait...")
      out= call.show_pending_event_status()
      out= json.loads(out)
      pending_events= out['pending_events']
      for pending_event in pending_events:
         text= "**"+pending_event['title']+"** \n"
         text+="{} out of {} members have accepted\n".format(pending_event['accepted'], pending_event['total'])
         text+= "Remaining: "
         for member in pending_event['remaining_members']:
            text+= member+", "
         buttons= [{
            'title': 'Show details',
            'payload': '/pending_event_details{"event_id":'+str(pending_event['id'])+'}'
         }]
         dispatcher.utter_button_message(
            text= text,
            buttons= buttons
         )
      return []



class EventDetailAction(Action):
   def name(self):
      return "action_event_details"

   def run(self, dispatcher, tracker, domain):
      dispatcher.utter_message("Fatching event details, please wait...")
      event_id= tracker.get_slot("event_id") 
      out= call.event_details(int(event_id))
      out= json.loads(out)
      if(out['status']=='success'):
         data= out['data']
         pout= "**"+data['title']+"**\n"
         dt= duck.str_to_dt(data['date_start'])
         ddt= dt.date()
         pout+= "Date: {}\n".format(ddt)
         ts= dt.strftime("%H:%M")
         te= duck.str_to_dt(data['date_end']).strftime("%H:%M")
         pout+= "Time: {} - {}\n".format(ts, te)
         pout+= "Members: _"
         for member in json.loads(data['members']):
            pout+= member+", "
         pout+= "\n **Bold** and *italic* and _pata_"
         dispatcher.utter_message(pout)
      else:
         dispatcher.utter_message("Error aa gyi") 


class PendingEventDetailAction(Action):
   def name(self):
      return "pending_event_detail_action"

   def run(self, dispatcher, tracker, domain):
      dispatcher.utter_message("Fatching event details, please wait...")
      event_id= tracker.get_slot("event_id") 
      out= call.pending_event_detail(int(event_id))
      out= json.loads(out) 
      if(out['status']=='error'):
         dispatcher.utter_message("Pending Event id is invalid")
         return []

      pe= out['data']
      text= "**"+pe['title']+"**\n"
      text+= "Status: {}/{}\n".format(pe['accepted'], pe['total'])
      text+= "Remaining: "
      for member in pe['remaining_members']:
         text+= member+", "
      text+= "\n"
      text+= "Accepted By: "
      for member in pe['accepted_by']:
         text+= member+ ", "
      dispatcher.utter_message(text)
      



class BusySlotAction(Action):
   def name(self):
      return "action_busy_slots"

   def run(self, dispatcher, tracker, domain):
      #dispatcher.utter_message("Fatching busy slots, please wait...")
      out= call.get_busy_slots()
      log.info("BusySlot OUT: {}".format(out))
      out= json.loads(out)
      if(len(out)==0):
         dispatcher.utter_message("Currently you don't have any busy slot")
      else:
         data= []
         week_days= {}
         for slot in out:
            ss= (slot['title'], slot['start_time'], slot['end_time'])
            if(ss not in data):
               data.append(ss)
               week_days[ss]= [slot['week_day']]
            else:
               temp= week_days[ss]
               temp.append(slot['week_day'])
               week_days[ss]= temp 
         log.info("WEEKOUT: {}".format(week_days))
         for wd in week_days:
            out_data=""
            title, ts, te= wd 
            wds= week_days[wd]
            out_data+= title+"\n"
            out_data+= str(ts)+" - "+str(te)+"\n"
            week_data= ""
            for ww in wds:
               week_data+= str(ww)
            week_data+="\n"
            out_data+= week_data
            log.info(out_data)
            dispatcher.utter_message(out_data)
      return []



class AASlotAction(Action):
   def name(self):
      return "action_aa_slots"

   def run(self, dispatcher, tracker, domain):
      #dispatcher.utter_message("Fatching aa slots, please wait...")
      out= call.get_aa_slots()
      log.info("AlwaysAvailable OUT: {}".format(out))
      out= json.loads(out)
      if(len(out)==0):
         dispatcher.utter_message("Currently you don't have any aa slot")
      else:
         data= []
         week_days= {}
         for slot in out:
            ss= (slot['title'], slot['start_time'], slot['end_time'])
            if(ss not in data):
               data.append(ss)
               week_days[ss]= [slot['week_day']]
            else:
               temp= week_days[ss]
               temp.append(slot['week_day'])
               week_days[ss]= temp 
         log.info("WEEKOUT: {}".format(week_days))
         for wd in week_days:
            out_data=""
            title, ts, te= wd 
            wds= week_days[wd]
            out_data+= title+"\n"
            out_data+= str(ts)+" - "+str(te)+"\n"
            week_data= ""
            for ww in wds:
               week_data+= str(ww)
            week_data+="\n"
            out_data+= week_data
            log.info(out_data)
            dispatcher.utter_message(out_data)

            
      
class LoginAction(Action):
   def name(self):
      return "action_login"

   def run(self, dispatcher, tracker, domain):
      user= tracker.get_slot("username")
      if(user is None):
         dispatcher.utter_message("Please specify the user")
         return []
      
      #dispatcher.utter_message("Logging as {}, please wait..".format(user))
      out= call.set_user(user)
      dispatcher.utter_message(out) 

      out= call.verify()
      out= json.loads(out)
      if(out['status']=='success'):
         dispatcher.utter_message("Welcome {}".format(out['user']))
      else:
         dispatcher.utter_message("Invalid User")


class VerifyAction(Action):
   def name(self):
      return "action_verify"

   def run(self, dispatcher, tracker, domain):
      dispatcher.utter_message("You are {}".format(call.user))
      return []



class TodaySchedule(Action):
   def name(self):
      return "action_today_schedule"

   def run(self, dispatcher, tracker, domain):
      
      today= duck.get_now().strftime("%Y-%m-%dT%H:%M")
      out= call.get_day_schedule(today)
      out= json.loads(out) 
      events= out['events']
      if(len(events)==0):
         dispatcher.utter_message("No meeting today")
         return []

      for data in events:
         pout= "**"+data['title']+"**\n"
         dt= duck.str_to_dt(data['date_start'])
         ddt= dt.date()
         pout+= "Date: {}\n".format(ddt)
         ts= dt.strftime("%H:%M")
         te= duck.str_to_dt(data['date_end']).strftime("%H:%M")
         pout+= "Time: {} - {}\n".format(ts, te)
         pout+= "Members: _"
         for member in json.loads(data['members']):
            pout+= member+", "
         pout+= "\n **Bold** and *italic* and _pata_"
         dispatcher.utter_message(pout)