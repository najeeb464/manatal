from django import forms 
from student.models  import Student,School

class StudentForm(forms.ModelForm):
    class Meta:
        model=Student
        fields=["first_name","last_name","auto_gen_identification","identification","dob","gender",
                "school","country","city","state","zip_code","address","phone","fax"]        
    def clean(self):
        auto_flag       =self.cleaned_data.get("auto_gen_identification",False)
        Identify_no     =self.cleaned_data.get("identification",None)
        schoolobj       =self.cleaned_data.get("school",None)
        if schoolobj:
             if schoolobj.student_set.only("id").all().exclude(id=self.id).count() > schoolobj.max_student_limit:
                 raise forms.ValidationError({'school':'Student Limit exceed in this school'})
        
        if  auto_flag == False:
            if  Identify_no is None or len(Identify_no) <=0:
                raise forms.ValidationError({'identification':'Please Either Provide Identification # or Choose  Auto gen Identification '})
            else:
                studentObj=Student.objects.filter(identification__exact=Identify_no)
                if self.instance and hasattr(self.instance,'pk'):
                    studentObj=studentObj.exclude(identification__exact=self.instance.identification)
                if studentObj.exists():
                    raise forms.ValidationError({'identification':'Student Identification must be unique'})
            
        return super().clean()

class SchoolForm(forms.ModelForm):
    class Meta:
        model=School
        fields=["name","country","city","state","zip_code","address","phone","fax"]
        
    def clean(self):
        _name=self.cleaned_data.get("name",None)
        if _name is None or len(_name)<=0:
            raise forms.ValidationError({'name':'School name is required'})
        else:
            schoolObj=School.objects.exclude(name__iexact=getattr(self.instance,'name',None)).filter(name__iexact=_name)
            if schoolObj.exists():
                raise forms.ValidationError({'school':'School name is required'})
            
        return super().clean()