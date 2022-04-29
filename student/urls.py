from rest_framework_nested import routers
from student.api.views import *
from django.urls import path,include

router = routers.SimpleRouter()
router.register(r'schools',SchoolViewSet)


school_router = routers.NestedSimpleRouter(router, r'schools', lookup='school')
school_router.register(r'students', StudentViewSet, basename='school-student')

urlpatterns = [
    path('gender/choices/', GenderChoicesView.as_view({'get': 'list'}),name="gender-choices"),
    path(r''              , include(router.urls)),
    path(r''              , include(school_router.urls)),
]