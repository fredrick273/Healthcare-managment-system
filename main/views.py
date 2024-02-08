from django.shortcuts import render,HttpResponse,redirect,resolve_url
from .models import Patient, Dept,Employee,Appointment
from django.contrib.auth.models import User

# Create your views here.

def home(request):
    return HttpResponse('Hello world')


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
    
    return render(request,'dept/new.html')

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
            Patient  = Patient.objects.get(id = request.POST.get('paitentid')),
            Doctor = Employee.objects.get(id = request.POST.get('doctor')),
            datetime = request.POST.get('date')
        )
        appointment.save()

        return HttpResponse(f"Appointment scheduled on {request.POST.get('date')}")
    patient = None
    doctors = Employee.objects.all().filter(Profession="Doctor")
    if 'id' in request.GET:
        patient_id = request.GET['id']
        try:
            patient = Patient.objects.get(id=patient_id)
        except Patient.DoesNotExist:
            pass

    
    
    return render(request, 'patient/op.html', {'patient': patient,'doctors':doctors})
