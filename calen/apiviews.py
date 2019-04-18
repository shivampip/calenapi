from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status 
from rest_framework import generics

from .models import Person, Event
from .serializers import PersonSerializer, EventSerializer

from dateutil.parser import parse
from datetime import timedelta

class CreatePerson(APIView):

    def post(self, request):
        #return Response(data= {"SHIVAM AGRAWAL"}, status= status.HTTP_200_OK)

        name= request.data.get("name")
        if(name is not None):
            fname, lname= name.split()
        else:
            fname= request.data.get("fname")
            lname= request.data.get("lname")
        
        data= {
            "fname": fname,
            "lname": lname
        }
        serializer= PersonSerializer(data= data)
        if(serializer.is_valid()):
            person= serializer.save()
            return Response(serializer.data, status= status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)


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
        author= request.data.get("author")
        title= request.data.get("title")
        date_start= request.data.get("date_start")
        date_end= request.data.get("date_end")

        self.check(date_start, date_end)

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
