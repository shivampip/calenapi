from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status 

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.http.response import HttpResponse, JsonResponse

from .models import Event, PendingEvent, Invite
from .serializers import EventSerializer, UserSerializer, PendingEventSerializer, InviteSerializer

import json 


from datetime import timedelta

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


    def process(self, data):
        requirements= []
        if('members' not in data):
            requirements.append({
                "field": "members",
                "msg": "Please specify the members"
            })
        if('duration' not in data):
            requirements.append({
                "field": "duration",
                "msg": "Please specify the duration"
            })
        if('time' not in data):
            requirements.append({
                "field": "time",
                "msg": "Please specify the time"
            })
        
        # If some requried fields are not given
        if(len(requirements)>0):
            result= {}
            result['status']= 'require'
            result['data']= 'data'
            return JsonResponse(result, status= status.HTTP_200_OK)

        # All fields are available, Now process
        # Call get available slots method


    def post(self, request):
        msg= request.POST.get('msg', None)
        data= {}
        if(msg is not None):

            data['msg']= msg 
            ##########################
            data['reply']= "Bot: {}".format(msg) 
            return JsonResponse(data , status= status.HTTP_202_ACCEPTED)
            ##########################

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

            self.process(res)

        person= request.POST.get('person', None)
        if(person is not None):
            return HttpResponse("person is "+person, status= status.HTTP_200_OK)
        return HttpResponse("Nothing found", status= status.HTTP_200_OK)