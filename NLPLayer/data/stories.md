
## Meeting
* set_meeting
  - utter_wait
  - meeting_manager
  - form{"name": "meeting_manager"}


##Greet
* greet
  - utter_greet


#List Events
* show_events
  - utter_thanks_for_pi


#Show Invites
* show_invites
  - show_invites_action

#Accept Invite
* accept_invite{"invite_id": "3"}
  - slot{"invite_id": "3"}
  - utter_ok
  - accept_invite_action