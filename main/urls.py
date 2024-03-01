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
    path('pharmacy/bill/',views.pharmacybill,name='pharmacybill')
    
    
]