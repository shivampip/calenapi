from django.shortcuts import render

import requests

from calen.mylog import log 

log.info("Inside Demo Views")


# Create your views here.

def make_url(path):
    return "http://localhost:8000/"+path 

def just_get(url):
    response= requests.get(url, headers= {'Authorization': "Token 7d257c1b1b8febefc09654eded7bb73957db17b1"})
    return response

def just_post(url, data):
    response= requests.post(url, data, headers= {'Authorization': "Token 7d257c1b1b8febefc09654eded7bb73957db17b1"})
    return response

def index(request):

    information = {
        'name': 'Shivam Agrawal',
        'city': 'Pipariya'
    }
    context= {'data': information}
    return render(request, 'demo/index.html', context)


def login(request):
    return render(request, "demo/login.html")


def register(request):
    return render(request, "demo/register.html")


def home(request):
    return render(request, "demo/home.html")



def create_event(request):
    return render(request, "demo/make_event.html") 

def create_pending_event(request):
    return render(request, "demo/make_pending_event.html")

def list_event(request):
    response= just_get(make_url("calen/le/"))
    context= {'data': response.json()}
    return render(request, "demo/list_events.html", context) 

def test(request):
    pass 

def show_invites(request):
    response= just_get(make_url("calen/si/"))
    context= {'data': response.json()}
    return render(request, "demo/show_invites.html", context) 
     


def accept_invite(request):
    pass  

def show_pending_event_status(request):
    pass 

def get_available_slots(request):
    return render(request, "demo/available_slots.html") 

def talk(request):
    type= request.POST.get('type', None)
    if(type is None):
        return render(request, "demo/talk.html")

    data= {}
    if(type == 'new'):
        log.info("New request")
        msg= request.POST.get('msg', None)
        log.info("Message is {}".format(msg)) 
        if(msg is None):
            return render(request, "demo/talk.html")   
        else:
            data['type']= 'new'
            data['msg']= msg 

    elif(type == 'update'):
        log.info("Upate request")
        data= {}
        data['type']= 'update'
        data['members']= request.POST.get('members', None) 
        data['from']= request.POST.get('from', None) 
        data['to']= request.POST.get('to', None)
        data['duration']= request.POST.get("duration", None) 
        data['title']= request.POST.get("title", None)                  
        data['include_author']= request.POST.get("include_author", None) 

    log.info("data is {}".format(str(data)))
    response= just_post(make_url('calen/bot/'), data)
    log.info("Received response")
    output= response.json()
    log.info("JSON parsed")
    status= output['status']
    log.info("Response output status is {}".format(status)) 
    if(status== 'require'):
        context= {'data': output}
        return render(request, "demo/talk.html", context) 
    elif(status== 'success'):
        context= {'data': output}
        return render(request, "demo/talk.html", context) 