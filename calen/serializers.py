from rest_framework import serializers
from rest_framework.authtoken.models import Token

from .models import Person, Event

from django.contrib.auth.models import User

class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model= Person
        fields= '__all__'


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model= Event
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