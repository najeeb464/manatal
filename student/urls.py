from rest_framework_nested import routers
from student.api.views import *
from django.urls import path,include

router = routers.SimpleRouter()
router.register(r'school',SchoolViewSet)


school_router = routers.NestedSimpleRouter(router, r'school', lookup='school')
school_router.register(r'student', StudentViewSet, basename='school-student')

urlpatterns = [
    path(r'', include(router.urls)),
    path(r'', include(school_router.urls)),
]