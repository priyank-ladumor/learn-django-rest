import django_filters
from employee.models import Employee
from blogs.models import Blogs

class EmployeeFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')
    designation = django_filters.CharFilter(field_name='designation', lookup_expr='icontains')
    
    class Meta:
        model = Employee
        fields = ['name', 'designation']
        
class BlogFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(field_name='title', lookup_expr='icontains') # check contains 
    status = django_filters.CharFilter(field_name='status', lookup_expr='iexact') # check exact but ignore case
    
    class Meta:
        model = Blogs
        fields = ['title', 'status']