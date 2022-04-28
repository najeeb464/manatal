from django_filters import rest_framework as filters
from student.models import *
from rest_framework.exceptions import ValidationError

class GeneralFilter(filters.FilterSet):
    country             =filters.CharFilter(field_name='country',label='Country',lookup_expr='icontains')
    city                =filters.CharFilter(field_name='city',label='City',lookup_expr='icontains')
    state               =filters.CharFilter(field_name='state',label='State',lookup_expr='icontains')
    zip_code            =filters.CharFilter(field_name='zip_code',label='Zip code',lookup_expr='startswith')
    
    class Meta:
        abstract=True
    

class SchoolFilter(GeneralFilter):
    name                =filters.CharFilter(field_name='name',label='Name',lookup_expr='icontains')
    class Meta:
        model=School
        fields=["name",'max_student_limit']