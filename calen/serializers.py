from rest_framework import serializers

from .models import Person, Event


class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model= Person
        fields= '__all__'


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model= Event
        fields= '__all__'