from django.shortcuts import render,HttpResponse,redirect,resolve_url,get_object_or_404
from .models import Patient, Dept,Employee,Appointment,PharmacyItem,PharmacyBill,PharmacyItemQuantity,Prescription,Test,LabTestResult,LabTestResultItem
from django.contrib.auth.models import User
from allauth.account.decorators import login_required
from django.conf import settings
import json


from django.http import JsonResponse
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet


# Create your views here.
Profession_types= (
    ("Doctor","Doctor"),
    ("Nurse","Nurse"),
    ("Reports","Reports"),
    ("Lab","Lab"),
    ("Pharamacy","Pharamacy"),
    ("Undefined","Undefined"),
)

def home(request):
    a = Appointment.objects.all().count()
    amt = 0
    for i in PharmacyBill.objects.all():
        amt += i.net_total
    p = Patient.objects.all().count()
    d = Employee.objects.all().filter(Profession="Doctor").count()

    return render(request,'dashboard/index.html',context={'a':a,'amt':amt,'p':p,'d':d})


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
    

    return render(request,'employee/new.html',context={'DepartmentList':Dept.objects.all(),'Profession_types':Profession_types})



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
            curr_item.curr_stock -= curr_quantity
            curr_item.save()
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

        return redirect('viewprescription',id=pres.id)


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


def newlabtest(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        units = request.POST.get('units')
        ref1 = request.POST.get('ref1')
        ref2 = request.POST.get('ref2')
        ref3 = request.POST.get('ref3')
        amount = request.POST.get('amt')

        if name and units and ref1 and amount:
            try:
                t = Test(name=name, units=units, ref1=ref1, ref2=ref2, ref3=ref3, amount=amount)
                t.save()
                return redirect('labtests')
            except Exception as e:
                return HttpResponse(f"An error occurred: {str(e)}")
        else:
            return HttpResponse("Incomplete data. Test not saved.")

    return render(request, 'lab/new.html')


def labtests(request):
    tests = Test.objects.all()
    for i in tests:
        print(i)
    return render(request,'lab/test.html',context={'tests':tests})


def labreport(request):

    t = Test.objects.all()
    d = Employee.objects.all().filter(Profession="Doctor")

    if request.method == 'POST':
        tests = json.loads(request.POST.get('items'))
        p = Patient.objects.get(id = request.POST.get('patient-id'))
        d = Employee.objects.get(id = request.POST.get('doctor'))
        ltr = LabTestResult(
            doctor = d,
            patient = p,
        )
        ltr.save()
        for i in tests:
            
            ltri = LabTestResultItem(
                test = Test.objects.get(id= i["id"]),
                result = ltr,
                value = i["value"]
            )
            ltri.save()

        return redirect('viewlabreport',id=ltr.id)
    d = Employee.objects.all().filter(Profession="Doctor")
    patient = None
    if 'id' in request.GET:
        patient_id = request.GET['id']
        try:
            patient = Patient.objects.get(id=patient_id)
        except Patient.DoesNotExist:
            pass
    return render(request,'lab/report.html',context={'doctors':d,'tests':t,'patient':patient})



def viewlabreport(request, id):
    lab_result = get_object_or_404(LabTestResult, id=id)

    # Create a PDF document
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="lab_report_{id}.pdf"'
    doc = SimpleDocTemplate(response, pagesize=letter)
    elements = []
    styles = getSampleStyleSheet()

    # Add lab report details
    elements.append(Paragraph(f"Patient: {lab_result.patient.Name}", styles['Normal']))
    elements.append(Paragraph(f"Doctor: {lab_result.doctor}", styles['Normal']))
    elements.append(Paragraph(f"Time: {lab_result.time}", styles['Normal']))
    elements.append(Paragraph("Test Results:", styles['Heading2']))

    # Retrieve test results for this lab report
    test_results = LabTestResultItem.objects.filter(result=lab_result)

    # Add test results to the document
    data = [['Test Name', 'Value', 'Ref 1', 'Ref 2', 'Ref 3']]
    for test_result in test_results:
        test_name = test_result.test.name
        test_value = test_result.value
        ref1 = test_result.test.ref1
        ref2 = test_result.test.ref2
        ref3 = test_result.test.ref3
        data.append([test_name, test_value, ref1, ref2, ref3])

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


def prescriptionhistory(request):
    patient = None
    prescription = None
    if 'id' in request.GET:
        patient_id = request.GET['id']
        try:
            patient = Patient.objects.get(id=patient_id)
            prescription = Prescription.objects.filter(patient = patient)
        except Patient.DoesNotExist:
            pass
    return render(request,'history/prescription.html',context={'prescriptions':prescription,'patient':patient})


def labhistory(request):
    patient = None
    labs = None
    if 'id' in request.GET:
        patient_id = request.GET['id']
        try:
            patient = Patient.objects.get(id=patient_id)
            labs = LabTestResult.objects.filter(patient = patient)
        except Patient.DoesNotExist:
            pass
    return render(request,'history/labreports.html',context={'reports':labs,'patient':patient})

def billhistory(request):
    patient = None
    bills = None
    if 'id' in request.GET:
        patient_id = request.GET['id']
        try:
            patient = Patient.objects.get(id=patient_id)
            bills = PharmacyBill.objects.filter(patient = patient)
        except Patient.DoesNotExist:
            pass
    return render(request,'history/bills.html',context={'bills':bills,'patient':patient})

def appointments(request):
    a = Appointment.objects.all()
    doctors = Employee.objects.all().filter(Profession="Doctor")
    if 'id' in request.GET:
        doc = request.GET['id']
        try:
            d = Employee.objects.get(id=doc)
            a = Appointment.objects.filter(Doctor = d)
        except Patient.DoesNotExist:
            pass

    return render(request,'patient/appointments.html',context={'appointments':a,'doctors':doctors})


def schedule(request):
    return render(request,'patient/schedule.html')

def get_item_details(request, item_id):
    item = get_object_or_404(PharmacyItem, pk=item_id)
    
    if request.method == 'POST':
        item.name = request.POST.get('name')
        item.price = request.POST.get('price')
        item.location = request.POST.get('loc')
        item.curr_stock = request.POST.get('stock')
        item.category = request.POST.get('category')
        item.save()
        return redirect('pharmacyitem')
        
    return render(request, 'edit_item_form.html', {'item':item})

