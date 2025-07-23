from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('employee', views.EmployeeViewSet, basename='employee')

urlpatterns = [
    path('students/', view=views.get_students),
    path('students/<int:id>', view=views.get_update_delete_student),
    
    # path('employee/', view=views.EmployeeList.as_view()),
    # path('employee/<int:pk>', view=views.EmployeeDetails.as_view()),
    
    path('', include(router.urls))
]
