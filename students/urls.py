from django.urls import path, include
from . import views

urlpatterns = [   
    path('', view=views.get_students, name='get_students'),
]