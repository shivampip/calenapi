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

'''
from duckling import DucklingWrapper

from hinlp.bot import MyBot
print("Importing NLU model....", end= "")
mb= MyBot()
mb.initNlu()
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
                    value= {'from': str(dsn), 'to': str(den)}      
                    result.append(value)

        return result



    def process(self, data, ruser):
        requirements= []
        if('members' not in data):
            requirements.append({
                "field": "members",
                "msg": "Please specify the members and try again."
            })
        if('duration' not in data):
            requirements.append({
                "field": "duration",
                "msg": "Please specify the duration and try again."
            })
        if('time' not in data):
            requirements.append({
                "field": "time",
                "msg": "Please specify the time and try again."
            })
        
        # If some requried fields are not given
        if(len(requirements)>0):
            result= {}
            result['status']= 'require'
            result['data']= requirements
            return JsonResponse(result, status= status.HTTP_200_OK)

        # All fields are available, Now process
        # Call get available slots method
        print("$$$$$ Everything is given")
        result= {}
        result['status']= 'accepted'
        result['data']= data 

        d_user= data['user']
        d_from= data['time']['from']
        d_to= data['time']['to']
        d_duration= data['duration']
        print("$$$$$ Values are extracted for user  {}".format(d_user))

        result= {}
        result['status']= 'success'


        available_slots= self.get_available_slots(ruser, d_from, d_to, d_duration)
        print("$$$$ Type is {}".format(type(available_slots)))
        #available_slots= json.dumps(available_slots)
        print("$$$$ Now type is {}".format(type(available_slots)))
        result['slots']= available_slots


        print("$$$$ Result prepared")
        print("$$$$ Result is {}".format(result))
        return result



    def post(self, request):
        msg= request.POST.get('msg', None)
        data= {}
        data['user']= str(request.user)
        if(msg is not None):

            data['msg']= msg 
            ##########################
            data['reply']= "Bot: {}".format(msg) 
            #return JsonResponse(data , status= status.HTTP_202_ACCEPTED)
            ##########################
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
            
            #############################
            
            res= {}
            res['user']= str(request.user)
            res['members']= ['shivam', 'gg']
            res['time']= {'from':'2019-04-24T06:00', 'to': '2019-04-25T11:30'}
            res['duration']= 7100

            #############################
            
            result= self.process(res, request.user)
            return JsonResponse(result, status= status.HTTP_200_OK)

        #person= request.POST.get('person', None)
        #if(person is not None):
        #    return HttpResponse("person is "+person, status= status.HTTP_200_OK)
        #return HttpResponse("Nothing found", status= status.HTTP_200_OK)