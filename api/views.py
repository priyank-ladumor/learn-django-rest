from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from students.models import Student
from .serializers import StudentSerializer
from rest_framework.response import Response
from rest_framework import status 
from rest_framework.decorators import api_view

@api_view(['GET', 'POST'])
def get_students(request):
    if request.method == 'GET':
        print('request method: ', request.method)
        students = Student.objects.all()
        serializer = StudentSerializer(students, many=True) # many=True for multiple objects get
        return Response(serializer.data, status=status.HTTP_200_OK)
    
        # # manually convert to json or serializer
        # student_list = list(students.values())
        # print('student_list: ', student_list)
        # # safe=False for non-dictionary data type to pass response
        # return JsonResponse(student_list, safe=False)
    
    elif request.method == 'POST':
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET', 'PUT', 'DELETE'])
def get_update_delete_student(request, id):
    try:
        student = Student.objects.get(pk=id)
    except Student.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = StudentSerializer(student)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif request.method == 'PUT':
        serializer = StudentSerializer(student, data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    elif request.method == 'DELETE':
        student.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)
