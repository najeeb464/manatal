from faker import Faker as FakerClass
from factory import django, Faker, post_generation,SubFactory

from student.models import School,Student

class SchoolFactory(django.DjangoModelFactory):
    max_student_limit = Faker('pyint', min_value=1, max_value=500)
    # max_student_limit =Fakerfuzzy.FuzzyInteger(10, 100)
    class Meta:
        model = School
    
    name=Faker('name')
    city=Faker('city')
    state=Faker('state')
    country=Faker('country')
    zip_code=Faker('zipcode')
    address=Faker('address')
    phone=Faker('phone_number')
    

class StudentFactory(django.DjangoModelFactory):
    
    class Meta:
        model = Student
    
    first_name=Faker('first_name')
    last_name=Faker('last_name')
    identification=Faker("pybool")
    
    school = SubFactory(SchoolFactory)
    city=Faker('city')
    state=Faker('state')
    country=Faker('country')
    zip_code=Faker('zipcode')
    address=Faker('address')
    phone=Faker('phone_number')
