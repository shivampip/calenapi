from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status 
from rest_framework import generics

from django.contrib.auth import authenticate
from django.http.response import HttpResponse

from .models import Event
from .serializers import EventSerializer, UserSerializer

from dateutil.parser import parse
from datetime import timedelta


class Home(APIView):
    def get(self, request):
        user= str(request.user)
        res= "<h2> Hello, Welcome "+user+"</h2>"
        return HttpResponse(res , status= status.HTTP_200_OK)



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