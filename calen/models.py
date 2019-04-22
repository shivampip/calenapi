from django.db import models
import json 

from django.contrib.auth.models import User

# Create your models here.


class Event(models.Model):
    author= models.ForeignKey(User, related_name= 'events', on_delete= models.CASCADE)
    title= models.CharField(max_length= 200)
    date_start= models.DateTimeField("From")
    date_end= models.DateTimeField("To")
    #members= models.ManyToManyField(User)
    members = models.CharField(max_length=200)

    '''
    def set_members(self, x):
        self.members = json.dumps(x)

    def get_members(self):
        return json.loads(self.members)
    '''

    def __str__(self):
        return self.title



class PendingEvent(models.Model):
    author= models.ForeignKey(User, related_name="pending_events", on_delete= models.CASCADE)
    title= models.CharField(max_length= 200)
    date_start= models.DateTimeField("From")
    date_end= models.DateTimeField("To")
    members= models.CharField(max_length= 200)


    def __str__(self):
        return self.title


class Invite(models.Model):
    pe= models.ForeignKey(PendingEvent, on_delete= models.CASCADE)
    ref= models.ForeignKey(User, on_delete= models.CASCADE)
    accepted= models.BooleanField('accepted', default=False)

    def __str__(self):
        return str(self.pe.title)+" for "+str(self.ref.username)