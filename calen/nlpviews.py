from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status 

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.http.response import HttpResponse, JsonResponse

from .models import Event, PendingEvent, Invite
from .serializers import EventSerializer, UserSerializer, PendingEventSerializer, InviteSerializer

import json 


from datetime import timedelta, datetime 
from dateutil.parser import parse 

from .mylog import log

log.debug("NLP Views")


'''
from duckling import DucklingWrapper
#from hinlp.bot import MyBot
print("Importing NLU model....", end= "")
#mb= MyBot()
#mb.initNlu()
print("DONE")
print("Importing Duckling.....", end= "")
dw= DucklingWrapper()
print("DONE")
'''

class Talk(APIView):

    def get_time(self, data):
        out={}
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
                    log.info('Before converting: {}'.format(in_value))
                    #out_from= datetime.strptime(in_value, "%Y-%m-%dT%H:%M")
                    #out_from= datetime.strptime(in_value, "YYYY-MM-DDTHH:MM:SS.mmmmmm")
                    # yyyy'-'MM'-'dd'T'HH':'mm':'ss'.'fffffffzz
                    out_from= parse(in_value)
                    log.info('After converting: {}'.format(out_from))
                    log.info('Type: {}'.format(type(out_from)))
                    out['to']= out_from + timedelta(days=1) 
                    log.info('Final to: {}'.format(out['to']))
        return out 
    


    def get_duration(self, data):
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


    def get_available_slots(self, user, start_date, end_date, duration):
        evs1= Event.objects.filter(author= user, date_start__range= (start_date, end_date))
        evs2= Event.objects.filter(author= user, date_start__range= (start_date, end_date))

        print("$$$$", 'evs1 and evs2 extravted len {}'.format(len(evs1)+len(evs2)))

        el1= [ev for ev in evs1]
        el2= [ev for ev in evs2]
        el= list(set(el1) | (set(el2)))

        na_slots= []
        for ev in el:
            ds= datetime.timestamp(ev.date_start)
            ct= datetime.fromtimestamp(ds)

            de= datetime.timestamp(ev.date_end)
            na_slots.append((ds, de))

        print("$$$$", 'NA_slots extracted len {}'.format(len(na_slots)))

        start_dt= datetime.strptime(start_date, "%Y-%m-%dT%H:%M")
        end_dt= datetime.strptime(end_date, "%Y-%m-%dT%H:%M")
        

        na_slots.append((0 , datetime.timestamp(start_dt)))
        na_slots.append((datetime.timestamp(end_dt), 0))
        na_slots.sort()

        result= []

        for i in range(1, len(na_slots)):
            my_start= na_slots[i-1][1]
            my_end= na_slots[i][0]
            if((my_end- my_start)>=duration):
                while((my_end- my_start)>=duration):
                    s_start= my_start
                    e_end= my_start+duration
                    my_start= e_end
                    dsn= datetime.fromtimestamp(s_start)
                    den= datetime.fromtimestamp(e_end)       
                    value= {'from': dsn.isoformat(), 'to': den.isoformat()}      
                    result.append(value)

        return result



    def process(self, data, ruser):
        log.info("Now processing")
        required= {
            'members': "Please specify the members",
            'duration': "You forgot the duration",
            'time': "Please mention time",
            'title': "Give a suitable title"
        }
        requirements= []
        found= []
        
        log.info("required defined")

        for field, message in required.items():
            if(field not in data):
                requirements.append({
                    "field": field,
                    "msg": message
                })
            else:
                # Parse them correctly. below
                if(field == "members"):
                    log.info('Before Member: {}'.format(data['members']))
                    log.info('After Mamber: {}'.format(data['members'][0]))
                    found.append({
                        "field": "members",
                        "value": data['members'][0]
                    })
                if(field == "time"):
                    found.append({
                        "field": "from",
                        "value": data['time']['from']
                    })
                    found.append({
                        "field": "to",
                        "value": data['time']['to']
                    })
                else:
                    found.append({
                        "field": field,
                        "value": data[field] # error aa sakti hai yaha
                    })
        
        log.info("Requirement: {} and Found: {}".format(len(requirements), len(found)))
        # If some requried fields are not given
        if(len(requirements)>0):
            result= {}
            result['status']= 'require'
            result['requirements']= requirements
            result['found']= found    
            return result

        log.info("Everythin is found")
        log.info("Data is {}".format(str(data)))

        d_user= data['user']
        d_from= data['time']['from']
        d_to= data['time']['to']
        d_duration= data['duration']

        result= {}
        result['status']= 'success'


        available_slots= self.get_available_slots(ruser, d_from, d_to, d_duration)
        result['slots']= available_slots
        result['members']= " ".join(data['members'])
        result['title']= data['title']
        result['include_author']= "checked" if data['include_author'] else " "

        return result

    

    def extract(self, msg):
        log.info("Extracting from msg")
        #out= mb.runNlu(msg)
        out= {}
        entities= out["entities"]
        res= {}
        # Members
        persons= []
        for entity in entities:
            if(entity['entity']=='person'):
                persons.append(entity['value'])
        #res['members']= persons 
        res['members']= " ".join(persons) 
        log.info('Extract member: {}'.format(res['members']))
        log.info('Members: {}'.format(str(persons)))
        # Time
        ttime= dw.parse_time(msg)
        res['time_raw']= ttime
        res['time']= self.get_time(ttime)
        log.info('Time: {}'.format(res['time']))
        # Duration
        duration= dw.parse_duration(msg)
        #res+= str(duration)
        res['duration_raw']= duration
        _, res['duration']= self.get_duration(duration)
        log.info('Duration: {}'.format(res['duration']))

        return res  


    def post(self, request):
        mtype= request.POST.get('type', None)
        res= {}

        log.info("mtype is {}".format(mtype))

        if(mtype== "new"):
            msg= request.POST.get("msg", None) 
            log.info("Now message is {}".format(msg))
            if(msg is not None):
                '''
                #Dummy data for testing
                log.info("Putting fake data") 
                res['user']= str(request.user)
                res['members']= ['shivam', 'gg']
                res['time']= {'from':'2019-04-27T06:00', 'to': '2019-04-29T11:30'}
                res['duration']= 7100
                res['title']= 'hello world title'
                res['include_author']= True  
                '''
                res= self.extract(msg)


        elif(mtype== "update"):
            r_members= request.POST.get('members', None) 
            r_from= request.POST.get('from', None) 
            r_to= request.POST.get('to', None)
            r_duration= request.POST.get("duration", None) 
            r_title= request.POST.get("title", None)                  
            r_include_author= request.POST.get("include_author", None)                 

            if(r_members is not None):
                log.info('Raw member is {}'.format(r_members))
                members= r_members
                #if(include_author):
                #    members.append(str(request.user))
                res['members']= r_members 
            if(r_from is not None and r_to is not None):
                res['time']= {'from': r_from, 'to': r_to }
            if(r_duration is not None):
                res['duration']= r_duration 
            if(r_title is not None):
                res['title']= r_title 
            if(r_include_author is not None):
                res['include_author']= r_include_author  
            

       
        '''
        out= mb.runNlu(msg)
        entities= out["entities"]
        res= {}
        # Members
        persons= []
        for entity in entities:
            if(entity['entity']=='person'):
                persons.append(entity['value'])
        res['members']= persons 
        # Time
        ttime= dw.parse_time(msg)
        res['time_raw']= ttime
        res['time']= self.get_time(ttime)
        # Duration
        duration= dw.parse_duration(msg)
        #res+= str(duration)
        res['duration_raw']= duration
        _, res['duration']= self.get_duration(duration)
        '''

        result= self.process(res, request.user)
        log.info("Result got. now sending JsonResponse") 
        return JsonResponse(result, status= status.HTTP_200_OK)
           