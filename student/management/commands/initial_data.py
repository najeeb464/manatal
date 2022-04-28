import random

from django.contrib.auth.models import User
from django.db import transaction
from django.core.management.base import BaseCommand

from student.models import School,Student
from student.factories import (
SchoolFactory,StudentFactory
)

NUM_SCHOOL=10
NUM_STUDENT =500

class Command(BaseCommand):
    help = "Initilizing Test Data"

    @transaction.atomic
    def handle(self, *args, **kwargs):
        self.stdout.write("Deleting old data...")
        models = [School, Student]
        for m in models:
            m.objects.all().delete()
        try:
            userObj=User.objects.get(email="test@gmail.com")
        except User.DoesNotExist:
            data={"username":"test","email":"test@gmail.com","is_staff":True,"is_superuser":True}
            userObj=User(**data)
            userObj.set_password("123456")
            userObj.save()
        except Exception as ex:
            self.stdout.write("exception occur",str(ex))
            

        self.stdout.write("Creating new data...")
        # Create all the school
        school_choices = []
        for _ in range(NUM_SCHOOL):
            schoolObj = SchoolFactory()
            school_choices.append(schoolObj)
        self.stdout.write("School data initilized.")

        # Create all the Student
        for _ in range(NUM_STUDENT):
            school = random.choice(school_choices)
            studentObj = StudentFactory(school=school)   
        self.stdout.write("Student data initilized.")    