from django.db import models
from django.contrib.auth.models import User

# Create your models here.

Sex_types = (
    ("Male", "Male"),
    ("Female", "Female"),
)

Patient_Marital = (
    ("Unmarried","Unmarried"),
    ("Married","Married"),
    ("Divorced", "Divorced"),
)

Profession_types= (
    ("Doctor","Doctor"),
    ("Nurse","Nurse"),
    ("Reports","Reports"),
    ("Lab","Lab"),
    ("Pharamacy","Pharamacy"),
    ("Undefined","Undefined"),
)

class Patient(models.Model):
    Name = models.CharField(max_length=512, null=True, blank=True)
    Dob = models.DateField(auto_now_add=False, null=True, blank=True)
    Sex = models.CharField(max_length=10, null=True, blank=True, choices=Sex_types)
    Mobile_nos = models.CharField(max_length=13,null=True, blank=True,default="+91")
    Alt_Mobile_nos = models.CharField(max_length=13,null=True, blank=True,default="+91")
    Address = models.CharField(max_length=200, null=True, blank=True)
    Age = models.IntegerField(null=True, blank=True) 
    Guardian = models.CharField(max_length=512, null=True, blank=True)
    Email = models.EmailField(null= True, blank=True)
    Marital_Status = models.CharField(max_length=100, null=True, blank=True, choices=Patient_Marital)
    Profession = models.CharField(max_length=100, null=True, blank=True)
    Created = models.DateTimeField(auto_now_add=True, null=True)



class Dept(models.Model):
    Name = models.CharField(max_length=100,blank=True,unique=True)

    def __str__(self):
        return f"{self.Name}"


class Employee(models.Model):
    User = models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True)
    Entry_No=models.IntegerField(null=True,blank=True)
    Profession=models.CharField(max_length=20,null=True,blank=True,choices=Profession_types)
    DOJ=models.DateField(blank=True,null=True)
    First_Name = models.CharField(max_length= 20, null=True, blank=True)
    Middle_Name=models.CharField(max_length= 20, null=True, blank=True)
    Last_Name=models.CharField(max_length= 20, null=True, blank=True)
    Gender=models.CharField(max_length=7,null=True,blank=True, choices=Sex_types)
    Blood_Group=models.CharField(max_length=10,null=True,blank=True)
    DOB=models.DateField(max_length=100,null=True)
    Religion=models.CharField(max_length=10,null=True,blank=True)
    Nationality=models.CharField(max_length= 20, null=True, blank=True)
    Address=models.CharField(max_length=100,null=True,blank=True)
    Pincode=models.IntegerField(blank=True,null=True)
    Email=models.EmailField(blank=True,null=True,)
    Department=models.ForeignKey(Dept, on_delete=models.CASCADE,null=True,blank=True)
    Details = models.CharField(max_length= 100, null=True, blank=True)
    Mobile = models.IntegerField(null=True, blank=True)
    AltMobile = models.IntegerField(null=True, blank=True)
    Marital_Status=models.CharField(max_length=100,null=True, blank=True, choices=Patient_Marital)
    Education_Details=models.CharField(max_length=100,blank=True)
    Experience_Details=models.CharField(max_length=100,blank=True)

    def __str__(self):
        return f"{self.First_Name} {self.Middle_Name} {self.Last_Name}"
    

class Appointment(models.Model):
    Patient = models.ForeignKey(Patient,on_delete=models.CASCADE,null=True,blank=True)
    Doctor = models.ForeignKey(Employee,on_delete=models.CASCADE,null=True,blank=True)
    datetime = models.DateTimeField(null=True)
