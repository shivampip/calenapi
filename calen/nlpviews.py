from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status 

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.http.response import HttpResponse

from .models import Event, PendingEvent, Invite
from .serializers import EventSerializer, UserSerializer, PendingEventSerializer, InviteSerializer

import json 

#from duckling import DucklingWrapper

from datetime import timedelta

'''
from hinlp.bot import MyBot
print("Importing NLU model....", end= "")
mb= MyBot()
mb.initNlu()
print("DONE")
print("Importing Duckling.....", end= "")
#dw= DucklingWrapper()
print("DONE")
'''

class Talk(APIView):


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
        return out 

    def get(self, request):
        msg= request.GET.get('msg', None)
        if(msg is not None):
            out= mb.runNlu(msg)
            entities= out["entities"]
            res= ""
            fields= ['person', 'time', 'duration']
            for entity in entities:
                name= entity['entity']
                value= entity['value']
                res+= name+": "+value+"<br>"
                if(name in fields):
                    fields.remove(name)
            res+= "Remaining fields: "+str(fields)

            res+="<br><br>Time<br>"
            res+= str(dw.parse_time(msg))

            res+="<br><br>Duration<br>"
            duration= dw.parse_duration(msg)
            res+= str(duration)

            res+= "<br><br>"+str(self.get_duration(duration))

            return HttpResponse(res, status= status.HTTP_200_OK)
        person= request.GET.get('person', None)
        if(person is not None):
            return HttpResponse("person is "+person, status= status.HTTP_200_OK)
        return HttpResponse("Nothign found", status= status.HTTP_200_OK)