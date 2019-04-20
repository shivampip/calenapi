from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status 
from rest_framework import generics

from django.contrib.auth import authenticate

from .models import Event
from .serializers import EventSerializer, UserSerializer

from dateutil.parser import parse
from datetime import timedelta


class CreateEventGen(generics.ListCreateAPIView):
    queryset= Event.objects.all()
    serializer_class= EventSerializer

class CreateEvent(APIView):
    
    def check(self, date_start, date_end):
        
        start_dt= parse(date_start)
        end_dt= parse(date_end)
        print("START DATE BEFORE {}".format(start_dt))
        start_dt= start_dt + timedelta(seconds= 1)
        print("START DATE AFTER {}".format(start_dt))

        
        evs= Event.objects.filter(date_start__range= (start_dt, end_dt))
        el= len(evs)
        evs= Event.objects.filter(date_end__range= (start_dt, end_dt))
        el+= len(evs)

        print("EVEVEVEV len is ", len(evs))
        if(len(evs)==0):
            return True
        return False 

    def post(self, request):
        #author= request.data.get("author")
        author= request.user
        title= request.data.get("title")
        date_start= request.data.get("date_start")
        date_end= request.data.get("date_end")

        is_slot_empty= self.check(date_start, date_end)
        if(not is_slot_empty):
            return Response({"Error": "Slot not empty"})

        data= {
            "author": author,
            "title": title,
            "date_start": date_start,
            "date_end": date_end
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

class CreateUser(generics.CreateAPIView):
    authentication_classes= ()
    permission_classes= ()
    serializer_class= UserSerializer



class LoginView(APIView):
    permission_classes= ()

    def post(self, request):
        username= request.data.get("username")
        password= request.data.get("password")
        user= authenticate(username= username, password= password)
        if(user):
            return Response({"token": user.auth_token.key}, status= status.HTTP_200_OK)
        else:
            return Response({"error": "Wrong credentials"}, status= status.HTTP_400_BAD_REQUEST)