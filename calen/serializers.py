from rest_framework import serializers
from rest_framework.authtoken.models import Token

from .models import Event, PendingEvent, Invite, BusySlot, AASlot

from django.contrib.auth.models import User


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model= Event
        fields= '__all__'


class PendingEventSerializer(serializers.ModelSerializer):
    class Meta:
        model= PendingEvent
        fields= '__all__'

class InviteSerializer(serializers.ModelSerializer):
    class Meta:
        model= Invite
        fields= '__all__'

class BusySlotSerializer(serializers.ModelSerializer):
    class Meta:
        model= BusySlot
        fields= '__all__'


class AASlotSerializer(serializers.ModelSerializer):
    class Meta:
        model= AASlot 
        fields= '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model= User
        fields= ('username', 'email', 'password')
        extra_kwargs= {'password': {'write_only': True}}

    def create(self, validated_data):
        user= User(
            email= validated_data['email'],
            username= validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        Token.objects.create(user= user)
        return user 