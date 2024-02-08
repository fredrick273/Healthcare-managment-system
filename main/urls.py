from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('register/',views.register),
    path('newdept/',views.newDept),
    path('newemp/',views.newemp),
    path('op/',views.op)
]