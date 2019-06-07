import requests
import json

from dateutil.parser import parse 
from datetime import timedelta, datetime 
from requests.exceptions import ConnectionError


USER_LOOKUP= {
    "shivam": "b554ba4b5b005776d8e61588d672cd86ebab4007",
    "sittu": "addecafcded82981e76368acdbf046dff5a368f8",
    "gg": "b26c611166dbbeb52331c35774f5b7dcf9a499ba",
    "ram": "8d0f8aceba340ed082ea541b4d5f752f9984715d"
}


class Caller:
    def __init__(self):
        user= 'ram'
        token= '8d0f8aceba340ed082ea541b4d5f752f9984715d'
        base_url= "http://localhost:8000/calen/"
        self.set(user, token, base_url)

    def set(self, user, token, base_url):
        self.user= user
        self.token= "Token {}".format(token) 
        self.base_url= base_url

    def set_user(self, user):
        if(user not in USER_LOOKUP):
            return "User not registered"
        else:
            self.user= user 
            self.token= "Token {}".format(USER_LOOKUP[user])
            return "User successfully logged in"


    def make_url(self, path):
        return self.base_url+path

    def just_get(self, url):
        response= requests.get(url, headers= {'Authorization': self.token})
        return response.content

    def just_post(self, url, data):
        try:
            response= requests.post(url, data, headers= {'Authorization': self.token})
            return response.content 
        except ConnectionError:
            response= {"status": "error", "error":"Unable to connect to Server. Make sure server is Online"}
            return json.dumps(response)
    
    
    def verify(self):
        url= self.make_url("verify/")
        out= self.just_get(url)
        return out

    def get_invites(self):
        url= self.make_url('show_invites/') 
        out= self.just_get(url) 
        return out

    def accept_invite(self, id):
        url= self.make_url('accept_invite?id={}'.format(id))        
        out= self.just_get(url) 
        return out 

    def show_pending_event_status(self):
        url= self.make_url('show_pending_event_status/')
        out= self.just_get(url)
        return out


    def event_details(self, id):
        url= self.make_url('event_details?id={}'.format(id))
        out= self.just_get(url)
        return out  

    def pending_event_detail(self, id):
        url= self.make_url('show_pending_event_status_one?id={}'.format(id))
        out= self.just_get(url)
        return out 
        
    def get_available_slots(self, start_dt, end_dt, duration):
        url= self.make_url('get_available_slots/')
        data={
            'start_date': start_dt,
            'end_date': end_dt,
            'duration': duration
        } 
        out= self.just_post(url, data)
        return out


    def get_best_available_slots(self, start_dt, end_dt, duration):
        url= self.make_url('get_best_available_slots/')
        data={
            'start_date': start_dt,
            'end_date': end_dt,
            'duration': duration
        } 
        out= self.just_post(url, data)
        return out

    def make_pending_event(self, title, dt_start, dt_end, include_author, members):
        url= self.make_url('make_pending_event/')
        data= {
            'title': title, 
            'date_start': dt_start,
            'date_end': dt_end,
            'include_author': include_author,
            'members': members
        }
        print("\n\nDATA SENDING ON SERVER IS : {}\n\n".format(str(data)))
        out= self.just_post(url, data)   
        return out 


    def get_busy_slots(self):
        url= self.make_url("get_busy_slots/")
        out= self.just_get(url) 
        return out 


    def get_aa_slots(self):
        url= self.make_url("get_aa_slots/")
        out= self.just_get(url) 
        return out 

    def get_notifications(self):
        url= self.make_url("notifications/")
        out= self.just_get(url)
        return out 
    

    def get_day_schedule(self, day):
        url= self.make_url("get_day_schedule/")
        data={
            "dt": day,
            "type": "all"
        }
        out= self.just_post(url, data) 
        return out 