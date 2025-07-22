from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

# Create your views here.

def get_students(request):
    students = {
        'first_name': 'John',
        'last_name': 'Doe'
    }
    return HttpResponse("<p>Hello from the students app!</p>")
