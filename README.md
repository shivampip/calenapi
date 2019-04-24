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

| Action  | Request type |  URL  |  arguments  | response | Authentication |
| ------------- | ------------- | ------------- | ------------- | ------------- | ------------- |
| Signup  | POST  | http://localhost:8000/signup/  |  username, password  | username  | False |
| Login  | POST  | http://localhost:8000/login/  |  username, password  | auth-token  | False |
| Home  | POST  | http://localhost:8000/  |  None  | html  | True |
| Verify user  | POST  | http://localhost:8000/home/  |  None  | html  |  True |
| Create Event  | POST  | http://localhost:8000/me/  |  title, date_start, date_end, members  | Ack  | True |
| List Event  | GET  | http://localhost:8000/le/  |  None  | Event list  | True |
| Show Invites  | GET  | http://localhost:8000/si/  |  None  | Invite list  | True |
| Accept Invite  | POST  | http://localhost:8000/ai/  |  id  | Ack  | True |
| Create Pending Event  | POST  | http://localhost:8000/mpe/  |  title, date_start, date_end, members, include_author  | Ack  | True |
| Pending Event Status  | GET  | http://localhost:8000/spes/  |  None  | All pending events status  | True |


## Progress

*  [![Generic badge](https://img.shields.io/badge/Authentication-ONGOING-1abc9c.svg)](https://shields.io/)
*  [![Generic badge](https://img.shields.io/badge/NLP-ONGOING-1abc9c.svg)](https://shields.io/)
*  [![Generic badge](https://img.shields.io/badge/Meeting_Management-ONGOING-1abc9c.svg)](https://shields.io/)
*  [![Generic badge](https://img.shields.io/badge/Framework-DONE-green.svg)](https://shields.io/)



## Diagram

![Scheduling flow](raw/VSchedule.png)
