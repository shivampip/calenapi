
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