
## Meeting
* set_meeting
  - utter_wait
  - meeting_manager
  - form{"name": "meeting_manager"}
  - form{"name": null}

## Just Book now
* book_meeting
  - action_book_meeting


## Meeting2
* set_meeting
  - utter_wait
  - meeting_manager
  - form{"name": "meeting_manager"}

## More Slots show
* show_more_slots
  - action_show_more_slots

## On Slot sleect
* select_slot{"timeframe":"timeframedata"}
  - slot{"timeframe":"timeframedata"}
  - action_select_slot


##Greet
* greet
  - utter_greet

##WhoAmI
* who_am_i
  - action_verify

#Show Invites
* show_invites
  - show_invites_action

#Accept Invite
* accept_invite{"invite_id": "3"}
  - slot{"invite_id": "3"}
  - utter_ok
  - accept_invite_action


#Show Notifications
* show_noti
  - action_noti


#Show Today Schedule
* show_today_schedule
  - action_today_schedule


#Show pending events status
* show_pending_events
  - show_pending_events_action
* pending_event_details{"event_id": "2"}
  - slot{"event_id": "2"} 
  - pending_event_detail_action



#Show Event details
* show_event_details{"event_id": "2"}
  - slot{"event_id": "2"}
  - action_event_details


#Show Busy Slots
* show_busy_slots
  - action_busy_slots

#Show AA Slots
* show_aa_slots
  - action_aa_slots

#Login
* login{"username":"shivam"}
  - slot{"username":"shivam"}
  - action_login

















<!------------------------------------------------------------------------------>
<!------------------------------------------------------------------------------>
<!------------------------------------------------------------------------------>
<!------------------------------------------------------------------------------>
<!------------------------------------------------------------------------------>


## say goodbye
* goodbye
  - utter_goodbye


##introduction
* introduction
  - utter_about_me

##Annoy
* annoying
  - utter_annoying


##Unhelpful
* unhelpful
  - utter_unhelpful

##Boring
* boring
  - utter_boring


##Boss
* boss
  - utter_boss

##ChatBot
* chatbot
  - utter_chatbot

##Smart
* smart
  - utter_thanks
  - utter_smart

##Good
* good
  - utter_good

##Marry
* marry
  - utter_marry

##Occupation
* occupation
  - utter_occupation

##Residence
* residence
  - utter_residence

##Bad
* bad
  - utter_bad

##Welldone
* welldone
  - utter_smile

##User happy
* happy
  - utter_me_happy

##User love agent
* love
  - utter_me_love

##Thanks
* thanks
  - utter_welcome

##Haal chal
* howru
  - utter_fine