from urllib import response
from django.test import TestCase

# Create your tests here.
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from student.factories import SchoolFactory,StudentFactory
from student.models import Student,School
from faker import Faker
from django.contrib.auth.models import User

import json

class SchoolTestCase(APITestCase):
    
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.client = APIClient()
        cls.school_url = reverse('school-list')
        for i in range(10):
            SchoolFactory()

    def test_ten_school(self):
        response = self.client.get(reverse('school-list'), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 10)
    def test_school_creation(self):
        schoolObj=SchoolFactory(name="SHS")
        data={
            "name":schoolObj.name,
            "max_student_limit":schoolObj.max_student_limit,
            "city":schoolObj.city,
            "country":schoolObj.country,
            "state":schoolObj.state,
            "address":schoolObj.address,
            "phone":schoolObj.phone
        }
       
        response = self.client.post(self.school_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        user_data={"username":"test","email":"test@gmail.com","password":"123456"}
        user=User.objects.create_superuser(**user_data)
        self.client.force_authenticate(user)
        response = self.client.post(self.school_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        data["name"]="Test School"
        response = self.client.post(self.school_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"],"Test School")
        
        new_obj = School.objects.get(name=data["name"])
        self.assertEqual(
            new_obj.max_student_limit,
           data["max_student_limit"],
        )
        data["name"]=""
        response = self.client.post(self.school_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        data["name"]="TEST"
        data["max_student_limit"]=-1
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    
    def test_detail_school(self):
        obj=SchoolFactory(name="BTS")
        user_data={"username":"test","email":"test@gmail.com","password":"123456"}
        user=User.objects.create_superuser(**user_data)
        self.client.force_authenticate(user)
        response=self.client.get(reverse('school-detail',kwargs={"pk":obj.id}),format='json')
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        response=self.client.get(reverse('school-detail',kwargs={"pk":10000000000}),format='json')
        self.assertEqual(response.status_code,status.HTTP_404_NOT_FOUND)
    
    def test_update_school(self):
        obj=SchoolFactory()
        response=self.client.put(reverse('school-detail',kwargs={"pk":obj.id}),data={"name":"Santa"},format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        user_data={"username":"test","email":"test@gmail.com","password":"123456"}
        user=User.objects.create_superuser(**user_data)
        self.client.force_authenticate(user)
        response=self.client.put(reverse('school-detail',kwargs={"pk":obj.id}),data={"name":"Santa"},format='json')
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
        response=self.client.put(reverse('school-detail',kwargs={"pk":obj.id}),data={"name":"Santa","max_student_limit":192},format='json')
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(response.data["name"],"Santa")
    
    def test_delete_school(self):
            obj=SchoolFactory(name="ROOTS")
            user_data={"username":"test","email":"test@gmail.com","password":"123456"}
            response=self.client.delete(reverse('school-detail',kwargs={"pk":obj.id}),format='json')
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
            user=User.objects.create_superuser(**user_data)
            self.client.force_authenticate(user)
            response=self.client.delete(reverse('school-detail',kwargs={"pk":obj.id}),format='json')
            self.assertEqual(response.status_code,status.HTTP_204_NO_CONTENT)
            response=self.client.delete(reverse('school-detail',kwargs={"pk":10000000000}),format='json')
            self.assertEqual(response.status_code,status.HTTP_404_NOT_FOUND)
        

from datetime import datetime
        
class StudentTestCase(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.client = APIClient()
        cls.gender_choice_url=reverse('gender-choices')
        # cls.student_url = reverse('student-list')
        for i in range(100):
            StudentFactory()
        
    def test_school_student_list(self):
        schoolObj=SchoolFactory(name="SHS")
        response = self.client.get(reverse('school-student-list',kwargs={"school_pk":schoolObj.id}), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    def test_student_creation(self):
        schoolObj=SchoolFactory(name="SHS")
        response = self.client.get(self.gender_choice_url, format='json')
        result=response.data
        data={
            "first_name": "student of",
            "last_name": " SHS",
            "dob":datetime.now().date(),
            "gender": result[0]["key"],
            "auto_gen_identification":True,
            "identification": "",
            "country": "",
            "city": "",
            "state": "",
            "zip_code": "",
            "address": "",
            "phone": "",
            "fax": ""}
        response = self.client.post(reverse('school-student-list',kwargs={"school_pk":schoolObj.id}),data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        user_data={"username":"test","email":"test@gmail.com","password":"123456"}
        user=User.objects.create_superuser(**user_data)
        self.client.force_authenticate(user)
        response = self.client.post(reverse('school-student-list',kwargs={"school_pk":schoolObj.id}),data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        data['auto_gen_identification']=False
        response = self.client.post(reverse('school-student-list',kwargs={"school_pk":schoolObj.id}),data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        data['first_name']=""
        data["last_name"]="" 
        response = self.client.post(reverse('school-student-list',kwargs={"school_pk":schoolObj.id}),data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_student_updation(self):
        # schoolObj=SchoolFactory(name="Model")
        response = self.client.get(self.gender_choice_url, format='json')
        # result=response.data
     
        obj=StudentFactory(first_name="Alex")
       
        
        response = self.client.get(reverse('school-student-detail',kwargs={"school_pk":obj.school.id,"pk":obj.id}), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["first_name"],obj.first_name)
        data={**response.data}
        data["first_name"]="Rough"
        response = self.client.put(reverse('school-student-detail',kwargs={"school_pk":obj.school.id,"pk":obj.id}),data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        user_data={"username":"test","email":"test@gmail.com","password":"123456"}
        user=User.objects.create_superuser(**user_data)
        self.client.force_authenticate(user)
        
        response = self.client.put(reverse('school-student-detail',kwargs={"school_pk":obj.school.id,"pk":obj.id}),data=data, format='json')
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        response = self.client.patch(reverse('school-student-detail',kwargs={"school_pk":obj.school.id,"pk":obj.id}),data={"last_name":"Bart"}, format='json')
        
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(response.data["last_name"],"Bart")
        

      

