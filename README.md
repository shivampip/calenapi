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

* Once server starts running, Browse at **http://localhost:8000/home/**
* Note: since its just backend, gui is not good. and gui is not available for all actions.


## API Documentation

| Action  | Request type |  URL  |  arguments  | response | Authentication |
| ------------- | ------------- | ------------- | ------------- | ------------- | ------------- |
| Signup  | POST  | http://localhost:8000/calen/signup/  |  username, password  | username  | False |
| Login  | POST  | http://localhost:8000/calen/login/  |  username, password  | auth-token  | False |
| Home  | POST  | http://localhost:8000/  |  None  | html  | True |
| Verify user  | POST  | http://localhost:8000/calen/home/  |  None  | html  |  True |
| Create Event  | POST  | http://localhost:8000/calen/me/  |  title, date_start, date_end, members  | Ack  | True |
| List Event  | GET  | http://localhost:8000/calen/le/  |  None  | Event list  | True |
| Show Invites  | GET  | http://localhost:8000/calen/si/  |  None  | Invite list  | True |
| Accept Invite  | POST  | http://localhost:8000/calen/ai/  |  id  | Ack  | True |
| Create Pending Event  | POST  | http://localhost:8000/calen/mpe/  |  title, date_start, date_end, members, include_author  | Ack  | True |
| Pending Event Status  | GET  | http://localhost:8000/calen/spes/  |  None  | All pending events status  | True |
| Get Available Slots  | POST  | http://localhost:8000/calen/as/  |  start_date, end_date, duration  | status, all available slots  | True |

Detailed formats will be provided, once its completed.

## Progress

*  [![Generic badge](https://img.shields.io/badge/Authentication-ONGOING-1abc9c.svg)](https://shields.io/)
*  [![Generic badge](https://img.shields.io/badge/NLP-ONGOING-1abc9c.svg)](https://shields.io/)
*  [![Generic badge](https://img.shields.io/badge/Meeting_Management-ONGOING-1abc9c.svg)](https://shields.io/)
*  [![Generic badge](https://img.shields.io/badge/Framework-DONE-green.svg)](https://shields.io/)



## Diagram

![Scheduling flow](raw/VSchedule.png)
