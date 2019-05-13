import requests


from dateutil.parser import parse 
from datetime import timedelta, datetime 

class Caller:
    def __init__(self):
        user= 'shivam'
        token= '7e556fd76814776d47907c2e2bc1c8ab39c7fc46'
        base_url= "http://localhost:8000/calen/"
        self.set(user, token, base_url)

    def set(self, user, token, base_url):
        self.user= user
        self.token= "Token {}".format(token) 
        self.base_url= base_url

    def make_url(self, path):
        return self.base_url+path

    def just_get(self, url):
        response= requests.get(url, headers= {'Authorization': self.token})
        return response

    def just_post(self, url, data):
        response= requests.post(url, data, headers= {'Authorization': self.token})
        return response
    
    
    def get_invites(self):
        url= self.make_url('show_invites/') 
        out= self.just_get(url) 
        return out.content

    def accept_invite(self, id):
        url= self.make_url('accept_invite?id={}'.format(id))
        out= self.just_get(url) 
        return out.content 

    def show_pending_event_status(self):
        url= self.make_url('show_pending_event_status/')
        out= self.just_get(url)
        return out.content

    def pending_event_detail(self, id):
        return "ID is {}, Welcome Shivam".format(id)
        

    

    