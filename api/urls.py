from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
'''
r'employee' means the URL path will begin with /employee/ & 
r (raw string) tells Python not to escape backslashes,
which is helpful if you're using regex patterns.
But in this case, 'users' and r'users' behave the same.
'''
router.register(r'employee', views.EmployeeViewSet, basename='employee')
router.register('blogs', views.BlogsViewSet, basename='blogs') 
router.register('comments', views.CommentViewSet, basename='comments')

urlpatterns = [
    path('students/', view=views.get_students),
    path('students/<int:id>', view=views.get_update_delete_student),
    
    # path('employee/', view=views.EmployeeList.as_view()),
    # path('employee/<int:pk>', view=views.EmployeeDetails.as_view()),
    
    path('', include(router.urls))
]
