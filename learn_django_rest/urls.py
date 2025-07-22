from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', view=views.home_view, name='home'), 
    path('admin/', admin.site.urls),
    
    # Web Application Endpoints
    path('students/', include('students.urls')),
    
    # API Endpoints
    path('api/v1/', include('api.urls'))
]
