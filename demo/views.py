from django.shortcuts import render

import requests

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
    msg= request.GET.get('msg')
    data= {'msg': msg}
    response= just_post(make_url("calen/bot/".format(msg)), data) 
    context= {'data': response.json()}
    jres= response.json()
    return render(request, "demo/talk.html", context) 