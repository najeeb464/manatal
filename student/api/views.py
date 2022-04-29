from student.api.serializers import SchoolSerializer, StudentSerializer
from rest_framework import viewsets,permissions
from student.filters import SchoolFilter,StudentFilter
from student.models import Student,School
from rest_framework.response import Response
from rest_framework.decorators import action


class GenderChoicesView(viewsets.ViewSet):
    pagination_class =None
    permission_classes = (permissions.AllowAny,)
    def list(self, request):
        return Response([{"key":i[0],"value":i[1]}for i in Student.GENDER_CHOICE])

class SchoolViewSet(viewsets.ModelViewSet):
    serializer_class = SchoolSerializer
    queryset         = School.objects.all().order_by('-id')
    filterset_class  = SchoolFilter
    permission_classes = (permissions.AllowAny,)
    
    def get_permissions(self):
        public_methods=['list','retrieve']
        if self.action in public_methods:
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

class StudentViewSet(viewsets.ModelViewSet):
    serializer_class = StudentSerializer
    permission_classes = (permissions.AllowAny,)
    filterset_class=StudentFilter
    def get_queryset(self):
        qs=Student.objects.filter(school__id=self.kwargs['school_pk']).order_by('-id')
        return Student.objects.filter(school__id=self.kwargs['school_pk']).order_by('-id')
    
    def get_permissions(self):
        public_methods=['list','retrieve']
        if self.action in public_methods:
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    
    @action(detail=False, methods=['GET'],name='choices')
    def gander_choices(self,*args,**kwargs):
        return Response([{"key":i[0],"value":i[1]}for i in Student.GENDER_CHOICE])
    
