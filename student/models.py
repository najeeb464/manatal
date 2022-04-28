from cProfile import label
from pyexpat import model
from sys import prefix
from tabnanny import verbose
from unittest import result
from django.db import models

import random
from django.core.validators import MinValueValidator

# Create your models here.

class GenericModelMixin(models.Model):
    created_at                          = models.DateTimeField(auto_now_add=True)
    updated_at                          = models.DateTimeField(auto_now=True)
    country                             =models.CharField(max_length=120,null=True,blank=True)
    city                                =models.CharField(max_length=120,null=True,blank=True)
    state                               =models.CharField(max_length=120,null=True,blank=True)
    zip_code                            =models.CharField(max_length=120,null=True,blank=True)
    address                             =models.CharField(max_length=120,null=True,blank=True)
    phone                               = models.CharField(max_length=100,null=True,blank=True)
    fax                                 =models.CharField(max_length=120,null=True,blank=True)
    class Meta:
        abstract = True

class School(GenericModelMixin):
    name            =models.CharField(max_length=120)
    max_student_limit  =models.PositiveIntegerField(validators=[MinValueValidator(1)])
    
    class Meta:
        verbose_name ="School"
        verbose_name_plural="Schools"
    
    def __str__(self):
        return self.name

class Student(GenericModelMixin):
    MALE='M'
    FEMALE='F'
    OTHER="O"
    GENDER_CHOICE=((MALE,"MALE"),(FEMALE,"FEMALE"),(OTHER,"OTHER"))
    
    first_name      =models.CharField(max_length=120)
    last_name       =models.CharField(max_length=120)
    auto_gen_identification  =models.BooleanField(default=True)
    identification  =models.CharField(max_length=20,blank=True)
    school          =models.ForeignKey(School,on_delete=models.CASCADE)
    dob             =models.DateField(null=True,blank=False)
    gender          =models.CharField(max_length=10,choices=GENDER_CHOICE,null=True,blank=False)
    
    class Meta:
        verbose_name ="Student"
        verbose_name_plural="Students"
        
    def __str__(self):
        return self.first_name+' '+self.last_name
    
    def display_gender(self):
        if self.gender:
            return dict(Student.GENDER_CHOICE)[self.gender]
        else:
            return ""
    def generate_pattern(self):
        school_prefix=str(self.school.name[0:2])+'-'+str(self.school.id)+'-'
        student_prefix='ST'+str(self.pk)+'-'
        filed_raange=range(0,20).stop
        result=str(school_prefix)+str(student_prefix)+str(random.randrange(1,filed_raange-(len(school_prefix)+len(student_prefix))))
        return result
        
    def save(self,*args,**kwargs):
        if self.pk:
            if self.auto_gen_identification:
                self.identification=self.generate_pattern()
            return super().save(*args,**kwargs)
        else:
            Obj=super().save(*args,**kwargs)
        self.save()
    
    