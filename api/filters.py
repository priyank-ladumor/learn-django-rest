import django_filters
from employee.models import Employee
from blogs.models import Blogs

class EmployeeFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')
    designation = django_filters.CharFilter(field_name='designation', lookup_expr='icontains')
    emp_id_min = django_filters.CharFilter(method='filter_by_emp_id_range', label='From Employee Id')
    emp_id_max = django_filters.CharFilter(method='filter_by_emp_id_range', label='To Employee Id')
    
    class Meta:
        model = Employee
        fields = ['name', 'designation', 'emp_id_max', 'emp_id_min']
        
    def filter_by_emp_id_range(self, queryset, name, value):
        if name == 'emp_id_min':
            return queryset.filter(emp_id__gte=value)
        elif name == 'emp_id_max':
            return queryset.filter(emp_id__lte=value)
        else:
            return queryset
        
class BlogFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(field_name='title', lookup_expr='icontains') # check contains 
    status = django_filters.CharFilter(field_name='status', lookup_expr='iexact') # check exact but ignore case
    id = django_filters.RangeFilter(field_name='id', lookup_expr='range') # only work on integers
    
    class Meta:
        model = Blogs
        fields = ['title', 'status', 'id']