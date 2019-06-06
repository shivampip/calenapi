from django.db import models
import json 

from django.contrib.auth.models import User

# Create your models here.


class Event(models.Model):
    author= models.ForeignKey(User, related_name= 'events', on_delete= models.CASCADE)
    title= models.CharField(max_length= 200)
    date_start= models.DateTimeField("From")
    date_end= models.DateTimeField("To")
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


class BusySlot(models.Model):
    author= models.ForeignKey(User, related_name= "busy_slot", on_delete= models.CASCADE)
    title= models.CharField(max_length= 200)
    week_day= models.PositiveIntegerField()
    start_time= models.TimeField()
    end_time= models.TimeField() 

    def __str__(self):
        return str(self.title)+" on "+str(self.week_day) 


class AASlot(models.Model):
    author= models.ForeignKey(User, related_name= "aa_slot", on_delete= models.CASCADE)
    title= models.CharField(max_length= 200)
    week_day= models.PositiveIntegerField()
    start_time= models.TimeField()
    end_time= models.TimeField() 

    def __str__(self):
        return str(self.title)+" on "+str(self.week_day) 


class Notification(models.Model):
    user= models.ForeignKey(User, related_name= "notification", on_delete= models.CASCADE)
    text= models.CharField(max_length= 500)
    seen= models.BooleanField()
    #link_text= models.CharField(max_length= 200)
    #link= models.CharField(max_length= 200)
    #link_data= models.CharField(max_length= 1500)
    data= models.CharField(max_length= 1000,  blank=True) 

    def __str__(self):
        return "For {}".format(self.user)+ ", {}".format(self.text)


class ShareableLink(models.Model):
    user= models.ForeignKey(User, related_name= "shareable_link", on_delete= models.CASCADE)
    title= models.CharField(max_length= 200)
    description= models.CharField(max_length= 1000)
    duration= models.IntegerField()

    def __str__(self):
        return self.title+" by "+str(self.user) 