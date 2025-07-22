from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from students.models import Student
from .serializers import StudentSerializer
from rest_framework.response import Response
from rest_framework import status 

def get_students(request):
    print('request: ', request)
    students = Student.objects.all()
    
    # # manually convert to json or serializer
    # student_list = list(students.values())
    # print('student_list: ', student_list)
    # # safe=False for non-dictionary data type to pass response
    # return JsonResponse(student_list, safe=False)

    serializer = StudentSerializer(students, many=True) # many=True for multiple objects get
    # return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.data)