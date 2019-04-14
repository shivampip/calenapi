from django.urls import path

from .apiviews import CreatePerson

urlpatterns = [
    path('createperson/', CreatePerson.as_view(), name='create_person'),
]
