from urllib import response
from django.test import TestCase

# Create your tests here.
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from student.factories import SchoolFactory
from student.models import Student,School
from faker import Faker
from django.contrib.auth.models import User

import json

class StudentTestCase(APITestCase):
    
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # cls.school_object = SchoolFactory.build()
        # cls.school_saved = SchoolFactory.create()
        cls.client = APIClient()
        cls.school_url = reverse('school-list')
        # cls.school_detail_url = reverse('school-detail',kwargs={"pk"})
        # cls.faker_obj = Faker()
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
        response = self.client.post(self.school_url)
        response=self.client.get(reverse('school-detail',kwargs={"pk":obj.id}),format='json')
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        response=self.client.get(reverse('school-detail',kwargs={"pk":10000000000}),format='json')
        self.assertEqual(response.status_code,status.HTTP_404_NOT_FOUND)
    
    def test_update_school(self):
        obj=SchoolFactory()
        response=self.client.put(reverse('school-detail',kwargs={"pk":obj.id}),data={"name":"Santa"},format='json')
        print("response data update",response)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        user_data={"username":"test","email":"test@gmail.com","password":"123456"}
        user=User.objects.create_superuser(**user_data)
        self.client.force_authenticate(user)
        response=self.client.put(reverse('school-detail',kwargs={"pk":obj.id}),data={"name":"Santa"},format='json')
        print("response",response.data)
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
        response=self.client.put(reverse('school-detail',kwargs={"pk":obj.id}),data={"name":"Santa","max_student_limit":192},format='json')
        print("response",response.data)
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(response.data["name"],"Santa")
        
        
    
        