from django.shortcuts import render,HttpResponse,redirect,resolve_url,get_object_or_404
from .models import Patient, Dept,Employee,Appointment,PharmacyItem,PharmacyBill,PharmacyItemQuantity,Prescription
from django.contrib.auth.models import User
from allauth.account.decorators import login_required
from django.conf import settings
import json

from django.http import HttpResponse
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet


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
    if request.method == 'POST':
        p = Patient.objects.get(id = request.POST.get('patient-id'))
        items = json.loads(request.POST.get('items'))
        bill = PharmacyBill(
            patient = p,
            itemcount = 0,
            net_total = 0
        )
        bill.save()
        amt = 0
        item_count = 0
        for i in items:
            curr_item = PharmacyItem.objects.get(id = int(i['id']))
            curr_quantity = int(i['quantity'])
            bill_item = PharmacyItemQuantity(
                bill= bill,
                item = curr_item,
                quantity = curr_quantity
            )
            bill_item.save()
            amt += curr_quantity * curr_item.price
            item_count += curr_quantity
        bill.net_total = amt
        bill.itemcount = item_count
        bill.save()
        return redirect('pharmacyviewbill',id=bill.id)

    p = PharmacyItem.objects.all()
    patient = None
    if 'id' in request.GET:
        patient_id = request.GET['id']
        try:
            patient = Patient.objects.get(id=patient_id)
        except Patient.DoesNotExist:
            pass
    return render(request,'pharmacy/bill.html',context={'items':p,'patient':patient})



def pharmacyviewbill(request, id):
    bill = get_object_or_404(PharmacyBill, id=id)

    # Create a PDF document
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="bill_{id}.pdf"'
    doc = SimpleDocTemplate(response, pagesize=letter)
    elements = []
    styles = getSampleStyleSheet()

    # Add bill details
    elements.append(Paragraph(f"Patient: {bill.patient.Name}", styles['Normal']))
    elements.append(Paragraph(f"Date: {bill.time}", styles['Normal']))
    elements.append(Paragraph("Items:", styles['Heading2']))

    # Add item details
    data = [['Item', 'Price', 'Quantity', 'Total']]
    total_cost = 0
    for item_quantity in bill.pharmacyitemquantity_set.all():
        item = item_quantity.item
        quantity = item_quantity.quantity
        total_item_cost = item.price * quantity
        total_cost += total_item_cost
        data.append([item.name, item.price, quantity, total_item_cost])

    # Add table to the document
    table = Table(data)
    style = TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.gray),
                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                        ('FONTNAME', (0, 0), (-1, 0), 'Courier-Bold'),
                        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                        ('GRID', (0, 0), (-1, -1), 1, colors.black)])
    table.setStyle(style)
    elements.append(table)

    # Add total cost
    elements.append(Paragraph(f"Total Cost: {total_cost}", styles['Normal']))

    # Build the PDF document
    doc.build(elements)
    return response


def prescription(request): 
    if request.method == 'POST':
        pres = Prescription(
            patient  = Patient.objects.get(id = request.POST.get('patientid')),
            doctor = Employee.objects.get(id = request.POST.get('doctor')),
            medications = request.POST.get('medications'),
            remarks = request.POST.get('remarks'),
            diagnosis = request.POST.get('diagnosis')
        )

        pres.save()

        return redirect(resolve_url('home'))


    doctors = Employee.objects.all().filter(Profession="Doctor")
   
    patient = None
    if 'id' in request.GET:
        patient_id = request.GET['id']
        try:
            patient = Patient.objects.get(id=patient_id)
        except Patient.DoesNotExist:
            pass
    return render(request,'prescription/new.html',context={'patient':patient,'doctors':doctors})



def view_prescription(request, id):
    prescription = get_object_or_404(Prescription, id=id)

    # Create a PDF document
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="prescription_{id}.pdf"'
    doc = SimpleDocTemplate(response, pagesize=letter)
    elements = []
    styles = getSampleStyleSheet()

    # Add prescription details
    elements.append(Paragraph(f"Patient: {prescription.patient.Name}", styles['Normal']))
    elements.append(Paragraph(f"Doctor: {prescription.doctor}", styles['Normal']))
    elements.append(Paragraph(f"Diagnosis: {prescription.diagnosis}", styles['Normal']))
    elements.append(Paragraph(f"Remarks: {prescription.remarks}", styles['Normal']))
    elements.append(Paragraph(f"Time: {prescription.time}", styles['Normal']))
    elements.append(Paragraph("Medications:", styles['Heading2']))

    # Parse medications JSON and add to the document
    if prescription.medications:
        medications_data = json.loads(prescription.medications)
        data = [['Name', 'Quantity', 'Morning', 'Afternoon', 'Night']]
        for med_data in medications_data:
            data.append([
                med_data.get('name', ''),
                med_data.get('quantity', ''),
                'Yes' if med_data.get('morning', False) else 'No',
                'Yes' if med_data.get('afternoon', False) else 'No',
                'Yes' if med_data.get('night', False) else 'No'
            ])
        # Add table to the document
        table = Table(data)
        style = TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.gray),
                            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                            ('FONTNAME', (0, 0), (-1, 0), 'Courier-Bold'),
                            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                            ('GRID', (0, 0), (-1, -1), 1, colors.black)])
        table.setStyle(style)
        elements.append(table)

    # Build the PDF document
    doc.build(elements)
    return response