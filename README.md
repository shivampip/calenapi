# calenapi
Scheduling Bot backend using Django Rest Framework


## Installation

* Clone the repo
```
git clone https://github.com/shivampip/calenapi.git
cd calenapi
```

* Installing dependancies
```
pip install -r requirements.txt
```

## Run

* Run server
```
python manage.py runserver
```

* Once server starts running, Browse at **http://localhost:8000/**
* Note: since its just backend, gui is not good. and gui is not available for all actions.


## API Documentation

| Action  | Request type |  URL  |  arguments  | response
| ------------- | ------------- | ------------- | ------------- | ------------- |
| Signup  | POST  | http://localhost:8000/signup/  |  username, password  | username  |
| Login  | POST  | http://localhost:8000/login/  |  username, password  | auth-token  |
| Home  | POST  | http://localhost:8000/  |  None  | html  |
| Verify user  | POST  | http://localhost:8000/home/  |  None  | html  |
| Create Event  | POST  | http://localhost:8000/me/  |  title, date_start, date_end, members  | Ack  |
| List Event  | GET  | http://localhost:8000/le/  |  None  | Event list  |
| Show Invites  | GET  | http://localhost:8000/si/  |  None  | Invite list  |
| Accept Invite  | POST  | http://localhost:8000/ai/  |  id  | Ack  |
| Create Pending Event  | POST  | http://localhost:8000/mpe/  |  title, date_start, date_end, members, include_author  | Ack  |
| Pending Event Status  | GET  | http://localhost:8000/spes/  |  None  | All pending events status  |




## Diagram

![Scheduling flow](raw/VSchedule.png)
