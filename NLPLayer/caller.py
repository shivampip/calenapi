import requests

#from duckling import DucklingWrapper
#dw= DucklingWrapper()

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

    def get_time(self, msg):
        data = dw.parse_time(msg)
        out= {}
        for dd in data:
            value= dd['value']
            in_value= value['value']

            if('grain' not in value):
                out['to']= in_value['to']
                out['from']= in_value['from']
            else:
                out['value']= in_value
                out['grain']= value['grain']

                grain= value['grain']
                out['from']= in_value 
                if(grain=='day'):
                    out_from= parse(in_value)
                    out['to']= out_from + timedelta(days=1) 
        return out 

    
    def get_duration(self, msg):
        data= dw.parse_duration(msg)
        out= ""
        total= 0
        for dd in data:
            out+= "Dimention: "+dd['dim']+"<br>"
            out+= "Text: "+dd['text']+"<br>"
            val= dd['value']
            tt= 0
            if(val['second'] is not None):
                tt+= timedelta(seconds= val['second']).total_seconds()
            elif(val['minute'] is not None):
                tt+= timedelta(minutes= val['minute']).total_seconds()
            elif(val['hour'] is not None):
                tt+= timedelta(hours= val['hour']).total_seconds()
            elif(val['day'] is not None):
                tt+= timedelta(days= val['day']).total_seconds()
            elif(val['month'] is not None):
                tt+= timedelta(months= val['month']).total_seconds()
            elif(val['year'] is not None):
                tt+= timedelta(years= val['year']).total_seconds()
            
            out+= "Duration in seconds: "+str(tt)+"<br>"
            total+= tt 
        out+= "<b>Total duration in seconds: "+str(total)+"</b><br>"
        return out, total 
    
    
    def get_invites(self):
        url= self.make_url('show_invites/') 
        out= self.just_get(url) 
        return out.content

    def accept_invite(self, id):
        url= self.make_url('accept_invite?id={}'.format(id))
        out= self.just_get(url) 
        return out.content 
        

    

    