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
        msg= request.GET['msg']
        out= mb.runNlu(msg)
        entities= out["entities"]
        res= ""
        for entity in entities:
            name= entity['entity']
            value= entity['value']
            res+= name+": "+value+"<br>"
        return HttpResponse(res, status= status.HTTP_200_OK)