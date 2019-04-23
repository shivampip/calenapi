from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status 
from rest_framework import generics

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.http.response import HttpResponse

from .models import Event, PendingEvent, Invite
from .serializers import EventSerializer, UserSerializer, PendingEventSerializer, InviteSerializer

from dateutil.parser import parse
from datetime import timedelta

from .hiutil import username_to_id
import json 


class CreateEventGen(generics.ListCreateAPIView):
    queryset= Event.objects.all()
    serializer_class= EventSerializer


class CreateEvent(APIView):
    
    def check(self, author, date_start, date_end):
        
        start_dt= parse(date_start)
        end_dt= parse(date_end)
        start_dt= start_dt + timedelta(seconds= 1)

        evs= Event.objects.filter(author= author, date_start__range= (start_dt, end_dt))
        el= len(evs)
        evs= Event.objects.filter(author= author, date_end__range= (start_dt, end_dt))
        el+= len(evs)

        print("EVEVEVEV len is ", len(evs))
        if(len(evs)==0):
            return True
        return False 

    def post(self, request):
        #author= request.data.get("author")
        author= request.user.id 
        title= request.data.get("title")
        date_start= request.data.get("date_start")
        date_end= request.data.get("date_end")
        include_author= request.data.get("include_author")
        
        raw_members= request.data.get("members")
        members= raw_members.split()
        if(include_author):
            members.append(str(request.user))

        is_slot_empty= self.check(author, date_start, date_end)
        if(not is_slot_empty):
            return Response({"Error": "Slot not empty"})

        data= {
            "author": author,
            "title": title,
            "date_start": date_start,
            "date_end": date_end,
            "members": json.dumps(members)
        }
        serializer= EventSerializer(data= data)
        if(serializer.is_valid()):
            event= serializer.save()
            return Response(serializer.data, status= status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)



class ListEvents(APIView):
    permission_classes= ()

    def get(self, request):
        user= request.user
        print("\nLIST\n {}".format(user))
        evs= Event.objects.filter(author= user)
        print("\nLIST\n {}".format(evs))
        serializer= EventSerializer(evs, many= True)
        return Response(serializer.data, status= status.HTTP_200_OK)



class TestEvent(APIView):
    def get(self, request):
        username= request.GET['name']
        print("USER is "+username)
        uid= username_to_id(username)
        print("USER ID is "+str(uid)) 

        evs= Event.objects.filter(author= uid)
        serializer= EventSerializer(evs, many= True)
        return Response(serializer.data, status= status.HTTP_200_OK)




class CreatePE(APIView):
    
    def check(self, author, date_start, date_end):
        
        start_dt= parse(date_start)
        end_dt= parse(date_end)
        start_dt= start_dt + timedelta(seconds= 1)

        pes= PendingEvent.objects.filter(author= author, date_start__range= (start_dt, end_dt))
        pel= len(pes)
        pes= PendingEvent.objects.filter(author= author, date_end__range= (start_dt, end_dt))
        pel+= len(pes)

        print("EVEVEVEV len is ", str(pel))
        if(pel==0):
            return True
        return False 


    def send_invite(self, pe, members, cuser):
        print("### Sending invite of "+str(pe))
        for member in members:
            # send invite
            user= User.objects.get(username= member)
            if(user==cuser):
                invite= Invite(pe= pe, ref= user, accepted= True)
            else:
                invite= Invite(pe= pe, ref= user, accepted= False)
            invite.save()
            print("### Invite sent to "+str(user.username))

    def post(self, request):
        #author= request.data.get("author")
        author= request.user.id 
        title= request.data.get("title")
        date_start= request.data.get("date_start")
        date_end= request.data.get("date_end")
        include_author= request.data.get("include_author")
        
        raw_members= request.data.get("members")
        members= raw_members.split()
        if(include_author):
            members.append(str(request.user))

        # Check for Event also 
        # This is check for PendingEvent
        is_slot_empty= self.check(author, date_start, date_end)
        if(not is_slot_empty):
            return Response({"Error": "Given time slot already contains a pending event"})

        data= {
            "author": author,
            "title": title,
            "date_start": date_start,
            "date_end": date_end,
            "members": json.dumps(members)
        }
        serializer= PendingEventSerializer(data= data)
        if(serializer.is_valid()):
            pe= serializer.save()
            self.send_invite(pe, members, request.user)
            return Response(serializer.data, status= status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)


class ShowPMSatus(APIView):
    def get(self, request):
        user= request.user
        pes= PendingEvent.objects.filter(author= user)
        out= ""
        for pe in pes:
            out+= "<h4>"+str(pe)+"</h4>"
            out+= "<table border= '1px solid black'>"
            invs= pe.invite_set.all()
            total= len(invs)
            accepted= 0
            for inv in invs:
                if(inv.accepted):
                    accepted+=1
                    out+= "<tr><td>"+str(inv.ref)+"</td><td>Accepted</td></tr>"
                else:
                    out+= "<tr><td>"+str(inv.ref)+"</td><td>Not accepted</td></tr>"
            out+= "</table>"
            out+= "<br><b>"+str(accepted)+" invites have been accepted out of "+str(total)+"</b>"
        if(out==""):
            return HttpResponse("No event")
        return HttpResponse(out)

class ShowInvites(APIView):
    def get(self, request):
        user= request.user
        invites= user.invite_set.all()
        serializer= InviteSerializer(invites, many= True)
        return Response(serializer.data, status= status.HTTP_200_OK)
        if(len(invites)<=0):
            return HttpResponse("No Invite")
        res= ""
        for invite in invites:
            res+= "<br>Your invite is "+str(invite)
        return HttpResponse(res)


class AcceptInvite(APIView):
    def get(self, request):
        user= request.user
        id= request.GET['id']
        invite = Invite.objects.get(id= id)
        if(invite.ref==user):
            invite.accepted= True   
            invite.save()
            return HttpResponse(str(invite)+" successfully accepted")
        else:
            return HttpResponse("Unauthenticated try")