from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('students/', view=views.get_students, name='get_students'),
    path('students/<int:id>', view=views.get_update_delete_student, name='get_update_delete_student'),
]
