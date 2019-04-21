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