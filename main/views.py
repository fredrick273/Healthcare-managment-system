from django.shortcuts import render,HttpResponse,redirect,resolve_url
from .models import Patient, Dept,Employee,Appointment,PharmacyItem
from django.contrib.auth.models import User
from allauth.account.decorators import login_required
from django.conf import settings
import json

# Create your views here.

def home(request):
    return render(request,'dashboard/index.html')


def register(request):
    if request.method == 'POST':
        pat = Patient(
                Name=request.POST["name"],
                Dob=request.POST["dob"],
                Sex=request.POST["gender"],
                Mobile_nos=request.POST["mobileno"],
                Alt_Mobile_nos=request.POST["alternateNo"],
                Address = request.POST["address"],
                Age = request.POST["age"],
                Guardian = request.POST["guardian"],
                Email = request.POST["email"],
                Marital_Status = request.POST["ismarried"],
                Profession= request.POST["profession"],
                )
        pat.save()

        return redirect(resolve_url('home'))
    return render(request,'patient/register.html')


def newDept(request):
    if request.method == 'POST':
        dept = Dept(
            Name = request.POST['name']
        )
        dept.save()
        return redirect(resolve_url('home'))
    dept = Dept.objects.all()
    return render(request,'dept/dept.html',context={'departments':dept})

def newemp(request):
    if request.method == 'POST':
        username = request.POST.get('user')
        email = request.POST.get('email')
        password1 = request.POST.get('pass')
        password2 = request.POST.get('pass2')

        # Validate form data
        if password1 != password2:
            return redirect('register')

        # Check if username is unique
        if User.objects.filter(username=username).exists():
            return redirect('register')

        # Check if email is unique
        if User.objects.filter(email=email).exists():
            return redirect('register')

        # Create user
        user = User.objects.create_user(username=username, email=email, password=password1)
        user.save()

        dept = Dept.objects.get(id=request.POST.get('Department'))

        emp = Employee(
            User = user,
            Department = dept,
            Entry_No = request.POST.get('entryno'),
            Profession = request.POST.get('profession'),
            DOJ = request.POST.get('DOJ'),
            First_Name = request.POST.get('fname'),
            Last_Name = request.POST.get('mname'),
            Middle_Name = request.POST.get('lname'),
            Gender = request.POST.get('Gender'),
            Blood_Group = request.POST.get('Blood_Group'),
            DOB= request.POST.get('DOB'),
            Religion = request.POST.get('religion'),
            Nationality = request.POST.get('Nationality'),
            Address = request.POST.get('address'),
            Pincode = request.POST.get('pincode'),
            Email = request.POST.get('email'),
            Mobile=request.POST.get('mob'),
            AltMobile = request.POST.get('altmob'),
            Marital_Status = request.POST.get('ismarried'),
            Education_Details = request.POST.get('Education'),
            Experience_Details = request.POST.get('Experience')
        )
        emp.save()

        return redirect(resolve_url('home'))
    

    return render(request,'employee/new.html',context={'DepartmentList':Dept.objects.all()})



def op(request):

    if request.method == 'POST':
        appointment = Appointment(
            Patient  = Patient.objects.get(id = request.POST.get('patientid')),
            Doctor = Employee.objects.get(id = request.POST.get('doctor')),
            datetime = request.POST.get('date')
        )
        appointment.save()

        return redirect('appointments')
    patient = None
    doctors = Employee.objects.all().filter(Profession="Doctor")
    if 'id' in request.GET:
        patient_id = request.GET['id']
        try:
            patient = Patient.objects.get(id=patient_id)
        except Patient.DoesNotExist:
            pass

    
    
    return render(request, 'patient/op.html', {'patient': patient,'doctors':doctors})

@login_required
def dashboard(request):
    user = request.user
    doc = Employee.objects.get(User=user)
    if doc.Profession == 'Doctor':
        appointments = Appointment.objects.filter(Doctor = doc)

        return render(request,'employee/dashboard.html',context={'appointments':appointments})
    return redirect(resolve_url('home'))


def patients(request):
    p = Patient.objects.all()
    return render(request,'patient/patients.html',context={'patients':p})

def employees(request):
    e = Employee.objects.all()
    return render(request,'employee/employees.html',context={'employees':e})


def appointments(request):
    a = Appointment.objects.all()
    return render(request,'patient/appointments.html',context={'appointments':a})

def pharmcyitem(request):
    if request.method == 'POST':
        p = PharmacyItem(
            name = request.POST.get('name'),
            price = request.POST.get('price'),
            location = request.POST.get('loc'),
            curr_stock = request.POST.get('stock'),
            category = request.POST.get('category')

        )

        p.save()

        return redirect('pharmacyitem')
    p = PharmacyItem.objects.all()
    return render(request,'pharmacy/newitem.html',context={'items':p})


def pharmacybill(request):
    items = {}
    p = PharmacyItem.objects.all()
    patient = None
    if 'id' in request.GET:
        patient_id = request.GET['id']
        try:
            patient = Patient.objects.get(id=patient_id)
        except Patient.DoesNotExist:
            pass
    return render(request,'pharmacy/bill.html',context={'items':p,'paitent':patient})