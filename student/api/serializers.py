from pyexpat import model
from django.urls import path, include
from rest_framework import routers, serializers, viewsets
from student.models import Student,School,GenericModelMixin


class ChoicesField(serializers.Field):
    def __init__(self, choices, **kwargs):
        self._choices = choices
        super(ChoicesField, self).__init__(**kwargs)

    def to_representation(self, obj):
        return self._choices[obj]

    def to_internal_value(self, data):
        return getattr(self._choices, data)

class SchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = School
        fields = ['id','name', 'max_student_limit','country',"city","state","zip_code","address","phone","fax"]
        def __init__(self, instance=None, *args, **kwargs):
            super().__init__(instance=instance,*args, **kwargs)
            request = self.context.get('request')
            if request and (request.method == 'POST' or request.method == 'PUT' or request.method == 'PATCH'):
                self.Meta.depth = 0
            else:
                self.Meta.depth = 1
        
    def validate(self, attrs):
        attrs=super().validate(attrs)
        print("attrs",attrs)
        name=attrs.get("name",None)
        schoolObj=School.objects.filter(name__iexact=name)
        if self.instance  and  hasattr(self.instance,'pk'):
            schoolObj=schoolObj.exclude(name__iexact=getattr(self.instance,'name'))
        if schoolObj.exists():
            raise serializers.ValidationError({"name":"School name must be unique"}) 
        return attrs
                
        
        
        
class StudentSerializer(serializers.ModelSerializer):
    # gander = ChoicesField(choices=[(i[0],i[1])for i in Student.GANDER_CHOICE])
    # stats=serializers.SerializerMethodField()
    # def get_stats(self,obj):
    #     return ''

    class Meta:
        model = Student
        fields = ['id', 'first_name', 'last_name','dob','gender','auto_gen_identification','identification','school','country',"city","state","zip_code","address","phone","fax"]
    def __init__(self, instance=None, *args, **kwargs):
        super().__init__(instance=instance,*args, **kwargs)
        request = self.context.get('request')
        if instance and hasattr(instance,"pk"):
            self.fields['identification'].read_only = True
            self.fields['auto_gen_identification'].read_only = True
            self.fields['school'].read_only = True
            
        if request and (request.method == 'POST' or request.method == 'PUT' or request.method == 'PATCH'):
            
            self.Meta.depth = 0
        else:
            self.Meta.depth = 1
    
    def validate(self, attrs):
        school_id = self.context['request'].parser_context['kwargs']['school_pk']
        if self.instance is None and not hasattr(self.instance,'pk'):
            if school_id:
                try:
                    schoolobj=School.objects.get(id=school_id)
                    if schoolobj.student_set.only("id").all().count() > schoolobj.max_student_limit:
                        raise serializers.ValidationError({"school":"Max Students Limit of School Exceeded"})         
                except School.DoesNotExist:
                    raise serializers.ValidationError({"school":"Invalid school choice"})
        return super().validate(attrs)
    