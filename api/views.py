from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from students.models import Student
from employee.models import Employee
from blogs.models import Blogs, Comments
from employee.serializers import EmployeeSerializer
from students.serializers import StudentSerializer
from blogs.serializers import BlogSerializer, CommentSerializer
from rest_framework.response import Response
from rest_framework import status 
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from django.http import Http404
from rest_framework import mixins, generics, viewsets
from .paginations import customPagination
from django_filters.rest_framework import DjangoFilterBackend
from .filters import EmployeeFilter, BlogFilter

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


# class EmployeeList(APIView):
#     def get(self, request):
#         employees = Employee.objects.all()
#         serializer = EmployeeSerializer(employees, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)
    
#     def post(self, request):
#         serializer = EmployeeSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
     
        
# class EmployeeDetails(APIView):
#     def get_object(self, pk):
#         try:
#             return Employee.objects.get(pk=pk)
#         except Employee.DoesNotExist:
#             raise Http404
        
#     def get(self, request, pk):
#         employee = self.get_object(pk)
#         serializer = EmployeeSerializer(employee)
#         return Response(serializer.data, status=status.HTTP_200_OK)
    
#     def put(self, request, pk):
#         employee = self.get_object(pk)
#         serializer = EmployeeSerializer(employee, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
#     def delete(self, request, pk):
#         employee = self.get_object(pk)
#         employee.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
    
'''
A Mixin is a reusable piece of code (a small class) that adds specific functionality to your view.
you pick only the tools (methods like .list(), .create(), etc.) you need
'''  
# class EmployeeList(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
#     queryset = Employee.objects.all() # default get
#     serializer_class = EmployeeSerializer # default serializer 
    
#     def get(self, request): # args and kwargs for extra arguments 
#         return self.list(request)
    
#     def post(self, request):
#         return self.create(request)
    

# class EmployeeDetails(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
#     queryset = Employee.objects.all()
#     serializer_class = EmployeeSerializer
    
#     def get(self, request, pk):
#         return self.retrieve(request, pk)
    
#     def put(self, request, pk):
#         return self.update(request, pk)
    
#     def delete(self, request, pk):
#         return self.destroy(request, pk)


'''
GenericAPIView is a special view that adds common features like:
    Handling queryset and serializer.
    Looking up objects by ID (pk).
    Integration with mixins (mixins need this to work).
    🔹 You combine GenericAPIView with mixins to create custom views.
'''

# class EmployeeList(generics.ListCreateAPIView):
#     queryset = Employee.objects.all()
#     serializer_class = EmployeeSerializer
#     # pagination_class = customPagination
    
# # class EmployeeDetails(generics.RetrieveAPIView, generics.UpdateAPIView, generics.DestroyAPIView):
# class EmployeeDetails(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Employee.objects.all()
#     serializer_class = EmployeeSerializer
#     lookup_field = 'pk'



'''
| Concept          | Description                                           | When to Use                   |
| ---------------- | ----------------------------------------------------- | ----------------------------- |
| **ViewSet**      | Group view logic (define your own list/retrieve/etc.) | When you need custom behavior |
| **ModelViewSet** | Auto CRUD for a model (queryset + serializer)         | For quick full-featured APIs  |
'''


# class EmployeeViewSet(viewsets.ModelViewSet):
#     queryset = Employee.objects.all()
#     serializer_class = EmployeeSerializer
    
    
class EmployeeViewSet(viewsets.ViewSet):
    def list(self, request):
        queryset = Employee.objects.all()

        # Apply filtering manually
        filtered_queryset = EmployeeFilter(request.GET, queryset=queryset).qs

        paginator = customPagination()
        page = paginator.paginate_queryset(filtered_queryset, request)

        if page is not None:
            serializer = EmployeeSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)
        
        serializer = EmployeeSerializer(filtered_queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def create(self, request):
        serializer = EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def retrieve(self, request, pk=None):
        # employee = Employee.objects.get(pk=pk)
        employee = get_object_or_404(Employee, pk=pk)
        serializer = EmployeeSerializer(employee)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def update(self, request, pk=None):
        employee = get_object_or_404(Employee, pk=pk)
        serializer = EmployeeSerializer(employee, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def destroy(self, request, pk=None):
        employee = get_object_or_404(Employee, pk=pk)
        employee.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    
    
class BlogsViewSet(viewsets.ModelViewSet):
    queryset = Blogs.objects.all()
    serializer_class = BlogSerializer
    pagination_class = customPagination
    lookup_field = 'pk'
    '''for default filter'''
    # filter_backends = [DjangoFilterBackend]
    # filterset_fields = ['title', 'status']
    
    '''for custom filter'''
    filterset_class = BlogFilter
    
class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comments.objects.all()
    serializer_class = CommentSerializer
    lookup_field = 'pk'
