
## Meeting
* set_meeting
  - utter_wait
  - meeting_manager
  - form{"name": "meeting_manager"}
* book_meeting
  - action_book_meeting


## Meeting2
* set_meeting
  - utter_wait
  - meeting_manager
  - form{"name": "meeting_manager"}
* show_more_slots
  - action_show_more_slots



##Greet
* greet
  - utter_greet


#List Events
* show_events
  - utter_thanks_for_pi


#Show Invites
* show_invites
  - show_invites_action
* accept_invite{"invite_id": "3"}
  - slot{"invite_id": "3"}
  - utter_ok
  - accept_invite_action


#Show pending events status
* show_pending_events
  - show_pending_events_action
* pending_event_details{"event_id": "2"}
  - slot{"event_id": "2"} 
  - pending_event_detail_action