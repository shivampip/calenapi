from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status 

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.http.response import HttpResponse

from .models import Event, PendingEvent, Invite
from .serializers import EventSerializer, UserSerializer, PendingEventSerializer, InviteSerializer

import json 

from hinlp.bot import MyBot
mb= MyBot()
mb.initNlu()

class Talk(APIView):
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
            return HttpResponse(res, status= status.HTTP_200_OK)
        person= request.GET.get('person', None)
        if(person is not None):
            return HttpResponse("person is "+person, status= status.HTTP_200_OK)
        return HttpResponse("Nothign found", status= status.HTTP_200_OK)