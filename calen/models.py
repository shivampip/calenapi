from django.db import models

# Create your models here.

class Person(models.Model):
    fname= models.CharField(max_length= 100)
    lname= models.CharField(max_length= 100)

    def __str__(self):
        return self.fname+ " "+ self.lname



class Event(models.Model):
    author= models.ForeignKey(Person, related_name= 'events', on_delete= models.CASCADE)
    title= models.CharField(max_length= 200)
    date_start= models.DateTimeField("From")
    date_end= models.DateTimeField("To")

    def __str__(self):
        return self.title