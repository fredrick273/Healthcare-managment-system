from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),

    path('patients/',views.patients,name='patients'),
    path('patients/register/',views.register,name='registerpatients'),
    
    path('employees/',views.employees,name='employees'),
    path('employees/register',views.newemp,name='registeremployees'),

    path('appointments/',views.appointments,name='appointments'),
    path('appointments/new/',views.op,name='newappointment'),

    path('department/',views.newDept,name='department'),
    
    path('dashboard/',views.dashboard),

    path('pharmacy/',views.pharmcyitem,name='pharmacyitem'),
    path('pharmacy/bill/',views.pharmacybill,name='pharmacybill'),
    path('pharmacy/bill/<int:id>/',views.pharmacyviewbill,name='pharmacyviewbill'),
    
    path('prescription/',views.prescription,name='prescription'),
    path('prescription/<int:id>/',views.view_prescription,name='viewprescription'),

    
    path('lab/new/',views.newlabtest,name='newlabtest'),
    path('lab/',views.labtests,name='labtests'),
    path('lab/report/',views.labreport,name='labreport'),
    path('lab/report/<int:id>/',views.viewlabreport,name='viewlabreport'),

    path('history/prescription/',views.prescriptionhistory,name='prescriptionhistory'),
    path('history/lab/',views.labhistory,name='labhistory'),
    path('history/bills/',views.billhistory,name='billhistory'),
]