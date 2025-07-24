from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# router = DefaultRouter(trailing_slash=False) # trailing_slash=False to remove url last or trailing slash
router = DefaultRouter() 

'''
r'employee' means the URL path will begin with /employee/ & 
r (raw string) tells Python not to escape backslashes,
which is helpful if you're using regex patterns.
But in this case, 'users' and r'users' behave the same.
'''
router.register('employee', views.EmployeeViewSet, basename='employee')
router.register('blogs', views.BlogsViewSet, basename='blogs') 
router.register('comments', views.CommentViewSet, basename='comments')

urlpatterns = [
    # Student APIs
    path('students/', views.get_students, name='student-list'),
    path('students/<int:id>/', views.get_update_delete_student, name='student-detail'),

    # Employee APIs
    # path('employee/', views.EmployeeListAPIView.as_view(), name='employee-list'),
    # path('employee/<int:pk>/', views.EmployeeDetailsAPIView.as_view(), name='employee-detail'),

    # Router URLs (if you're using ViewSets somewhere)
    path('', include(router.urls)),
]
