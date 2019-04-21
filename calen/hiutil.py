
from django.contrib.auth.models import User

def username_to_id(username):
    return User.objects.get(username= username)


